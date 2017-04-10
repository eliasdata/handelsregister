# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from geo_views import migrate


def delete_views(_, _args, **_kwargs):
    """
    Some views need manual destruction
    """
    migrations.DeleteModel('BetrokkenPersonen')
    migrations.DeleteModel('DataSelectieView'),
    migrations.DeleteModel('SbicodesPerVestiging'),


def create_pass(_, _args, **_kwargs):
    """
    Created in the operations..
    """
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('hr', '__first__'),
        ('hr', '0002_geovestigingen'),
        ('hr', '0007_dataselectie'),
    ]

    operations = [
        # set the site name
        # migrations.RunPython(code=create_site, reverse_code=delete_site),

        # delete manual view
        # NOTE BetrokkenPersonen
        migrations.RunPython(code=create_pass, reverse_code=delete_views),

        # create the hr views
        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties",
            sql="""SELECT * FROM hr_geovestigingen"""
        ),

        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_bouw",
            sql="""
SELECT * FROM hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
        'bouw/utiliteitsbouw algemeen / klusbedrijf',
        'bouw overig',
        'bouwinstallatie',
        'afwerking van gebouwen',
        'dak- en overige gespecialiseerde bouw',
        'grond, water, wegenbouw',
        'bouw/utiliteitsbouw algemeen / klusbedrijf')
"""
        ),

        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_overheid_onderwijs_zorg",
            sql="""
SELECT * FROM hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
        'onderwijs',
        'gezondheids- en welzijnszorg',
        'overheid')
"""
        ),

        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_productie_installatie_reparatie",     # noqa
            sql="""
SELECT * FROM hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
        'installatie (geen bouw)',
        'reparatie (geen bouw)',
        'productie')
"""
        ),

        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_zakelijke_dienstverlening",
            sql="""
    SELECT * FROM hr_geovestigingen
    WHERE hr_geovestigingen.sbi_detail_group in (
            'arbeidsbemiddeling, uitzendbureaus, uitleenbureaus',
            'overige zakelijke dienstverlening',
            'reclame en marktonderzoek',
            'interieurarchitecten',
            'managementadvies, economisch advies',
            'technisch ontwerp, advies, keuring/research',
            'design',
            'public relationsbureaus',
            'advocaten rechtskundige diensten, notarissen',
            'architecten',
            'accountancy, administratie')
    """
        ),

        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_handel_vervoer_opslag",
            sql="""
SELECT * FROM hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
        'vervoer',
        'detailhandel (verkoop aan consumenten, niet zelf vervaardigd)',
        'handelsbemiddeling (tussenpersoon, verkoopt niet zelf)',
        'opslag',
        'dienstverlening vervoer',
        'handel en reparatie van auto s',
        'groothandel (verkoop aan andere ondernemingen, niet zelf vervaardigd)'
        )
"""
        ),

        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_landbouw",
            sql="""
SELECT * FROM hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
        'teelt eenjarige gewassen',
        'gemengd bedrijf',
        'teelt sierplanten',
        'dienstverlening voor de land/tuinbouw',
        'teelt meerjarige gewassen',
        'fokken, houden dieren')
"""
        ),

        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_persoonlijke_dienstverlening",
            sql="""
SELECT * FROM hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
        'sauna, solaria',
        'schoonheidsverzorging',
        'uitvaart, crematoria',
        'overige dienstverlening',
        'kappers')
"""
        ),
        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_informatie_telecommunicatie",
            sql="""
SELECT * FROM hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
    'activiteiten op het gebied van ict',
    'activiteiten  op gebied van film, tv, radio, audio',
    'telecommunicatie',
    'uitgeverijen')
"""
        ),
        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_cultuur_sport_recreatie",
            sql="""
SELECT * FROM hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
        'sport',
        'musea, bibliotheken, kunstuitleen',
        'kunst',
        'recreatie')
"""
        ),
        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_financiele_dienstverlening_verhuur",    # noqa
            sql="""
SELECT * FROM hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
        'verhuur van- en beheer/handel in onroerend goed',
        'verhuur van roerende goederen',
        'holdings (geen financiële)',
        'holdings, financiële dienstverlening en verzekeringen')
"""
        ),
        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_overige",
            sql="""
SELECT * FROM hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
    'idieële organisaties',
    'belangenorganisaties',
    'overige',
    'hobbyclubs')
"""
        ),
        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_horeca",
            sql="""
SELECT * FROM hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
    'hotel-restaurant',
    'overige horeca',
    'kantine, catering',
    'cafetaria, snackbar, ijssalon',
    'café',
    'hotel, pension',
    'restaurant, café-restaurant')
"""
        ),

        # NAAM QUERIES

        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_naam",
            sql="""
SELECT row_number() OVER () AS id, geometrie, naam, locatie_type
from hr_geovestigingen
GROUP BY geometrie, naam, locatie_type
    """
        ),

        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_bouw_naam",
            sql="""
    SELECT row_number() OVER () AS id, geometrie, naam, locatie_type
    from hr_geovestigingen
    WHERE hr_geovestigingen.sbi_detail_group in (
            'bouw/utiliteitsbouw algemeen / klusbedrijf',
            'bouw overig',
            'bouwinstallatie',
            'afwerking van gebouwen',
            'dak- en overige gespecialiseerde bouw',
            'grond, water, wegenbouw',
            'bouw/utiliteitsbouw algemeen / klusbedrijf')
    GROUP BY geometrie, naam, locatie_type
        """
        ),

        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_overheid_onderwijs_zorg_naam",
            sql="""
SELECT row_number() OVER () AS id, geometrie, naam, locatie_type
from hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
        'onderwijs',
        'gezondheids- en welzijnszorg',
        'overheid')
GROUP BY geometrie, naam, locatie_type
    """
        ),

        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_productie_installatie_reparatie_naam",     # noqa
            sql="""
SELECT row_number() OVER () AS id, geometrie, naam, locatie_type
from hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
        'installatie (geen bouw)',
        'reparatie (geen bouw)',
        'productie')
GROUP BY geometrie, naam, locatie_type
    """
        ),

        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_zakelijke_dienstverlening_naam",           # noqa
            sql="""
SELECT row_number() OVER () AS id, geometrie, naam, locatie_type
from hr_geovestigingen
    WHERE hr_geovestigingen.sbi_detail_group in (
            'arbeidsbemiddeling, uitzendbureaus, uitleenbureaus',
            'overige zakelijke dienstverlening',
            'reclame en marktonderzoek',
            'interieurarchitecten',
            'managementadvies, economisch advies',
            'technisch ontwerp, advies, keuring/research',
            'design',
            'public relationsbureaus',
            'advocaten rechtskundige diensten, notarissen',
            'architecten',
            'accountancy, administratie')
GROUP BY geometrie, naam, locatie_type
        """
    ),

        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_handel_vervoer_opslag_naam",
            sql="""
SELECT row_number() OVER () AS id, geometrie, naam, locatie_type
from hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
        'vervoer',
        'detailhandel (verkoop aan consumenten, niet zelf vervaardigd)',
        'handelsbemiddeling (tussenpersoon, verkoopt niet zelf)',
        'opslag',
        'dienstverlening vervoer',
        'handel en reparatie van auto s',
        'groothandel (verkoop aan andere ondernemingen, niet zelf vervaardigd)'
        )
GROUP BY geometrie, naam, locatie_type
    """
        ),

        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_landbouw_naam",
            sql="""
SELECT row_number() OVER () AS id, geometrie, naam, locatie_type
from hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
        'teelt eenjarige gewassen',
        'gemengd bedrijf',
        'teelt sierplanten',
        'dienstverlening voor de land/tuinbouw',
        'teelt meerjarige gewassen',
        'fokken, houden dieren')
GROUP BY geometrie, naam, locatie_type
    """
        ),

        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_persoonlijke_dienstverlening_naam",   # noqa
            sql="""
SELECT row_number() OVER () AS id, geometrie, naam, locatie_type
from hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
        'sauna, solaria',
        'schoonheidsverzorging',
        'uitvaart, crematoria',
        'overige dienstverlening',
        'kappers')
GROUP BY geometrie, naam, locatie_type
    """
        ),
        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_informatie_telecommunicatie_naam",     # noqa
            sql="""
SELECT row_number() OVER () AS id, geometrie, naam, locatie_type
from hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
    'activiteiten op het gebied van ict',
    'activiteiten  op gebied van film, tv, radio, audio',
    'telecommunicatie',
    'uitgeverijen')
GROUP BY geometrie, naam, locatie_type
    """
    ),
        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_cultuur_sport_recreatie_naam",
            sql="""
SELECT row_number() OVER () AS id, geometrie, naam, locatie_type
from hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
        'sport',
        'musea, bibliotheken, kunstuitleen',
        'kunst',
        'recreatie')
GROUP BY geometrie, naam, locatie_type
    """
    ),
        # Note afwijkende naam ivm. maximale lengte
        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_financiele_dienstverlening_verhuur_na", # noqa
            sql="""
SELECT row_number() OVER () AS id, geometrie, naam, locatie_type
from hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
        'verhuur van- en beheer/handel in onroerend goed',
        'verhuur van roerende goederen',
        'holdings (geen financiële)',
        'holdings, financiële dienstverlening en verzekeringen')
GROUP BY geometrie, naam, locatie_type
    """
    ),
        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_overige_naam",
            sql="""
SELECT row_number() OVER () AS id, geometrie, naam, locatie_type
from hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
    'idieële organisaties',
    'belangenorganisaties',
    'overige',
    'hobbyclubs')
GROUP BY geometrie, naam, locatie_type
    """
    ),
        migrate.ManageView(
            view_name="geo_hr_vestiging_locaties_horeca_naam",
            sql="""
SELECT row_number() OVER () AS id, geometrie, naam, locatie_type
from hr_geovestigingen
WHERE hr_geovestigingen.sbi_detail_group in (
    'hotel-restaurant',
    'overige horeca',
    'kantine, catering',
    'cafetaria, snackbar, ijssalon',
    'café',
    'hotel, pension',
    'restaurant, café-restaurant')
GROUP BY geometrie, naam, locatie_type
    """
        ),

    # Dataselectie view
    migrate.ManageView(
        view_name="hr_betrokken_personen",
        sql="""
SELECT row_number() OVER (ORDER BY (( SELECT 1))) AS id,
   mac.naam AS mac_naam,
   mac.kvk_nummer,
   mac.datum_aanvang,
   mac.datum_einde,
   vs.id AS vestiging_id,
   vs.vestigingsnummer,
   p1.id AS persoons_id,
   p1.rol,
       CASE
           WHEN p1.naam IS NOT NULL THEN p1.naam
           WHEN p2.naam IS NOT NULL THEN p2.naam
           WHEN np1.geslachtsnaam IS NOT NULL THEN np1.geslachtsnaam
           ELSE NULL::character varying
       END AS naam,
   p1.rechtsvorm,
   fv.functietitel,
   fv.soortbevoegdheid,
   np2.geslachtsnaam AS bevoegde_naam
  FROM hr_maatschappelijkeactiviteit mac
    JOIN hr_vestiging vs ON vs.maatschappelijke_activiteit_id = mac.id
    JOIN hr_persoon p1 ON mac.eigenaar_id = p1.id
    LEFT JOIN
        hr_natuurlijkpersoon np1 ON np1.id::text = p1.natuurlijkpersoon_id::text
    LEFT JOIN
        hr_functievervulling fv ON fv.heeft_aansprakelijke_id = mac.eigenaar_id
    LEFT JOIN
        hr_persoon p2 ON fv.is_aansprakelijke_id = p2.id
    LEFT JOIN
        hr_natuurlijkpersoon np2 ON np2.id::text = p2.natuurlijkpersoon_id::text
        """),    # noqa
    ]
