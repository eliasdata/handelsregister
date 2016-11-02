import factory
import random

from django.contrib.gis.geos import Point

from factory import fuzzy

from .. import models


class NatuurlijkePersoon(factory.DjangoModelFactory):
    class Meta:
        model = models.NatuurlijkPersoon

    id = fuzzy.FuzzyInteger(low=10000000000000, high=10000000000099)
    voornamen = 'piet'


class PersoonFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Persoon

    id = fuzzy.FuzzyInteger(low=100000000000000000, high=100000000000000099)
    faillissement = False


class MaatschappelijkeActiviteitFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.MaatschappelijkeActiviteit

    id = fuzzy.FuzzyInteger(low=100000000000000000, high=100000000000000099)
    kvk_nummer = fuzzy.FuzzyInteger(low=1, high=99999999)


class VestigingFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Vestiging

    id = fuzzy.FuzzyInteger(low=100000000000000000, high=100000000000000099)
    vestigingsnummer = fuzzy.FuzzyInteger(low=1, high=9999999)
    hoofdvestiging = fuzzy.FuzzyChoice(choices=[True, False])
    maatschappelijke_activiteit = factory.SubFactory(
        MaatschappelijkeActiviteitFactory)

    @factory.post_generation
    def activiteiten(self, create, activiteiten=None, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if activiteiten:
            # A list of groups were passed in, use them
            for a in activiteiten:
                self.activiteiten.add(a)


class LocatieFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Locatie

    id = fuzzy.FuzzyInteger(low=100000000000000000, high=100000000000000099)

    afgeschermd = fuzzy.FuzzyChoice(choices=[True, False])

    bag_numid = fuzzy.FuzzyChoice(choices=[1, 2])  # 'put_in_fixture_id'
    bag_vbid = fuzzy.FuzzyChoice(choices=[3, 4])  # 'put_in_fixture_id'


class Activiteit(factory.DjangoModelFactory):
    class Meta:
        model = models.Activiteit

    id = fuzzy.FuzzyInteger(low=100000000000000000, high=100000000000000099)
    sbi_code = '1073'

    hoofdactiviteit = fuzzy.FuzzyChoice(choices=[True, False])


class FunctievervullingFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Functievervulling

    id = fuzzy.FuzzyInteger(low=100000000000000000, high=100000000000000099)


class SBIHoofdcatFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.CBS_sbi_hoofdcat
    hcat = 'jan'
    hoofdcategorie = 'sub bla'


class SBISubcatFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.CBS_sbi_subcat

    scat = 'piet'
    hcat = factory.SubFactory(SBIHoofdcatFactory)
    subcategorie = 'sub bla'


class SBIcatFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.CBS_sbicodes

    sbi_code = fuzzy.FuzzyInteger(low=20000, high=40099)
    sub_sub_categorie = 'bla'
    scat = factory.SubFactory(SBISubcatFactory)


def create_x_vestigingen(x=5):
    """
    Create some valid vestigingen with geo-location and sbi_codes

    RANDOM
    """

    vestigingen = []

    mac = MaatschappelijkeActiviteitFactory.create()
    # SBIcatFactory.create()
    a1 = Activiteit.create(sbi_code='1073')

    point = Point(121944.32, 487722.88)

    for i in range(x):

        loc_b = LocatieFactory.create(
                id='{}{}'.format('b', i),
                bag_numid=i,
                bag_vbid=i,
                geometrie=point
        )

        loc_p = LocatieFactory.create(
                id=i*100+1,
                bag_numid='p{}'.format(i),
                bag_vbid='p{}'.format(i),
                geometrie=point
        )

        for v in range(random.randint(1, 10)):
            ves = VestigingFactory.create(
                id='{}-{}'.format(i, v),
                bezoekadres=loc_b,
                postadres=loc_p,
                activiteiten=[a1],
                maatschappelijke_activiteit=mac
            )

            vestigingen.append(ves)

    return vestigingen


def create_dataselectie_set():

    # THIS IS A RANDOM AMOUNT
    create_x_vestigingen(x=5)

    macs = models.MaatschappelijkeActiviteit.objects.all()
    persoon = PersoonFactory.create()
    persoon.natuurlijkpersoon = NatuurlijkePersoon.create()

    models.Vestiging.objects.all()

    for m in macs:
        m.eigenaar = persoon
        m.save()

    return persoon


def create_search_test_locaties():
    """
    Create some test data for the location search completer
    """

    # locatie zonder geo maar met
    # adres en geo in fixture
    loc_1 = LocatieFactory.create(
        id='{}{}'.format('b', 1),
        bag_numid=None,
        bag_vbid=None,
        geometrie=None,
        correctie=None,
        volledig_adres='ikbestaniet 10, 1013AW, Amsterdam'
    )

    # locatie zonder geo en geen adres
    # in atlas fixture
    loc_2 = LocatieFactory.create(
        id=2*100+1,
        bag_numid=None,
        bag_vbid=None,
        geometrie=None,
        correctie=None,
        volledig_adres='ikbestawel 10 A, 1013AW, Amsterdam'

    )

    return [loc_1, loc_2]
