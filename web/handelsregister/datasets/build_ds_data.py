
import logging

from itertools import groupby
from datetime import datetime, date
from django import db
from decimal import Decimal
import time
from django.contrib.gis.geos.point import Point

from datasets.hr.models import DataSelectie
from datasets.hr.models import GeoVestigingen
from datasets.hr.models import CBS_sbi_hoofdcat
from datasets.hr.models import BetrokkenPersonen

log = logging.getLogger(__name__)

VESTIGING_FIELDS = ('vestigingsnummer', 'naam', 'hoofdvestiging',
                    'locatie_type', 'geometrie', 'bag_vbid')

BETROKKENEN_FIELDS = ('mac_naam', 'rol', 'naam', 'rechtsvorm', 'functietitel',
                      'soortbevoegdheid', 'bevoegde_naam')

MAATSCHAPPELIJKE_ACT_FIELDS = ('kvk_nummer', 'datum_aanvang', 'datum_einde')

LOCATIE_FIELDS = (
    'straat_huisnummer', 'huisletter', 'huisnummer', 'huisnummertoevoeging',
    'postcode', 'straatnaam', 'postbus_nummer', 'toevoegingadres',
    'volledig_adres', 'correctie', 'afgeschermd')

PROGRESSREPORT = 10         # report every xx seconds


def to_dict(data: object, fields: tuple) -> dict:
    result_dict = {}
    for f in fields:
        value = getattr(data, f)
        if isinstance(value, Point):
            value = [value.x, value.y]
        elif isinstance(value, Decimal):
            value = str(value)
        elif isinstance(value, datetime) or isinstance(value, date):
            value = value.isoformat()
        result_dict[f] = value

    return result_dict


def flatten_sbi():
    """
    Flatten sbicodes
    """
    log.info('Flatten sbicodes')
    sbi_values = {}
    for hoofdcat in CBS_sbi_hoofdcat.objects.select_related():
        for subcat in hoofdcat.cbs_sbi_subcat_set.all():
            for sbi in subcat.cbs_sbicodes_set.all():
                sbi_values[sbi.sbi_code] = {
                    'sbi_code': sbi.sbi_code,
                    'hoofdcategorie': hoofdcat.hoofdcategorie,
                    'subcategorie': subcat.subcategorie,
                    'sub_sub_categorie': sbi.sub_sub_categorie,
                    'hcat': hoofdcat.hcat,
                    'scat': subcat.scat}
    return sbi_values


def _build_joined_ds_table():
    """
    De dataselectie wordt in 2 stappen geschreven. Eerst wordt de api data
    opgebouwd en in een json met een key per vestiging_id weggeschreven.

    Vervolgens wordt in dataselectie deze file gelezen en worden de
    search keys opgenomen in elastic, waardoor die doorzoekbaar wordt
    in dataselectie.
    """

    with db.connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE hr_dataselectie")

    sbi_values = flatten_sbi()

    betrokken_per_vestiging = (
        BetrokkenPersonen.objects.order_by('vestigingsnummer').iterator())

    # Indien geen betrokkenen -> resultaat is None
    try:
        betrokken = next(betrokken_per_vestiging)
    except StopIteration:
        betrokken = None

    totalrowcount = GeoVestigingen.objects.filter(locatie_type='B').count()

    log.info('START opbouw dataselectie api als json:  %s', totalrowcount)

    # groupby vestigings nummer
    by_vestiging = groupby(
        GeoVestigingen.objects.filter(locatie_type='B')
        .order_by('vestigingsnummer'),
        lambda row: row.vestigingsnummer
    )

    count = 1
    lastreport = time.time()

    for vestigingsnummer, vest_data in by_vestiging:

        count, lastreport = measure_progress(totalrowcount, count, lastreport)

        # verzamel gegevens per vestiging
        vst_sbi, vestiging_dict, naam, bag_vbid = per_vestiging(
            vestigingsnummer, vest_data, sbi_values)

        # save json in ds tabel
        write_hr_dataselectie(
            vst_sbi, betrokken, vestiging_dict,
            vestigingsnummer, betrokken_per_vestiging, naam, bag_vbid)

    log.info('Opbouw dataselectie api als json VOLTOOID')


def per_vestiging(vestigingsnummer, vest_data, sbi_values):
    """
    Read data per vestiging and build dict (to be json) per
    vestiging
    """

    first = True
    vst_sbi = []

    for sbi_repeat in vest_data:

        if first:
            vestiging_dict = to_dict(sbi_repeat, VESTIGING_FIELDS)
            vestiging_dict = add_adressen_dict(vestiging_dict, sbi_repeat)
            vestiging_dict['sbi_codes'] = vst_sbi = []
            first = False

        sbi = sbi_values[sbi_repeat.sbi_code]
        sbi['vestigingsnummer'] = vestigingsnummer
        sbi['bedrijfsnaam'] = sbi_repeat.naam

        vst_sbi.append(sbi)

    return vst_sbi, vestiging_dict, sbi_repeat.naam, sbi_repeat.bag_vbid


def write_hr_dataselectie(
        vst_sbi, betrokken, vestiging_dict, vestigingsnummer,
        betrokken_per_vestiging, naam, bag_vbid):

    if len(vst_sbi):
        vestiging_dict = add_betrokkenen_to_vestigingen(
                betrokken, vestiging_dict,
                vestigingsnummer, betrokken_per_vestiging)
    else:
        log.error('Vestiging %s %s zonder sbi code' % (vestigingsnummer, naam))

    if vestiging_dict and bag_vbid:
        ds = DataSelectie(vestigingsnummer, bag_vbid, vestiging_dict)
        ds.save()


def measure_progress(totalrowcount, count, lastreport):
    """
    Every PROGRESSREPORT timedelta print progres line
    """
    count += 1

    if time.time() - lastreport > PROGRESSREPORT:
        lastreport = time.time()
        pct_complete = str(int((count * 100) / totalrowcount)) + '%'

        log.info('Opbouw dataselectie %s voltooid, rownr %s',
                 pct_complete, count)

    return count, lastreport


def add_adressen_dict(vestiging_dict: dict, sbi_repeat) -> dict:
    """
    Voeg bezoek- en postadressen toe als dict aan resulterende json.
    bezoekadres en postadres zijn relaties van geolocatie, de gevonden rijen
    worden vertaald naar dict.
    """

    if sbi_repeat.bezoekadres and sbi_repeat.bezoekadres.bag_nummeraanduiding:
        bezoekadres = to_dict(sbi_repeat.bezoekadres, LOCATIE_FIELDS)
        vestiging_dict['bezoekadres'] = bezoekadres
    else:
        vestiging_dict['bezoekadres'] = None

    if sbi_repeat.postadres and sbi_repeat.postadres.bag_nummeraanduiding:
        postadres = to_dict(sbi_repeat.postadres, LOCATIE_FIELDS)
        vestiging_dict['postadres'] = postadres
    else:
        vestiging_dict['postadres'] = None

    return vestiging_dict


def add_betrokkenen_to_vestigingen(
        betrokken, vestiging_dict, vestigingsnummer,
        betrokken_per_vestiging) -> dict:
    """
    Voeg betrokkenen aan vestiging toe. Let op, dit is een balanceline
    verwerking. Om de snelheid hoog te houden lees ik de betrokkenen
    per vestiging in en verwerk ze voor de vestiging waar ik mee
    bezig ben. Vergelijkbaar met een join op SQL.
    De oplossing is gekozen vanwege complexiteit (en traagheid) van
    de resulterende join in SQL tegenover de snelheid van sequentiele
    verwerking
    """

    vestiging_dict['betrokkenen'] = vst_betr = []
    first = True

    while betrokken and betrokken.vestigingsnummer <= vestigingsnummer:
        if betrokken.vestigingsnummer == vestigingsnummer:
            vst_betr.append(to_dict(betrokken, BETROKKENEN_FIELDS))
            if first:
                mac_dict = to_dict(betrokken, MAATSCHAPPELIJKE_ACT_FIELDS)
                vestiging_dict.update(mac_dict)
                first = False
        try:
            betrokken = next(betrokken_per_vestiging)
        except StopIteration:
            break

    return vestiging_dict
