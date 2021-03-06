from decimal import Decimal

from django.test import TestCase

from datasets import build_hr_data
from datasets.kvkdump import models as kvk
from datasets.kvkdump import utils
from .. import models


class ImportFunctievervullingTest(TestCase):
    def setUp(self):
        utils.generate_schema()

    @staticmethod
    def _convert(fvv: kvk.KvkFunctievervulling) -> models.Functievervulling:
        build_hr_data.fill_stelselpedia()
        return models.Functievervulling.objects.get(id=fvv.ashid)

    def test_import_typical_example(self):
        kvk.KvkPersoon.objects.get_or_create(
            prsid=Decimal('200000000000000000'),
            prshibver=Decimal('100000000000000000'),
            faillissement='Nee',
            naam='Testpersoon 1 B.V.',
            persoonsrechtsvorm='BeslotenVennootschap',
            rsin='000000001',
            typering='rechtspersoon',
            uitgebreiderechtsvorm='BeslotenVennootschap',
            verkortenaam='Testpersoon 1 Verkort B.V.',
            volledigenaam='Testpersoon 1 Volledig B.V.',
            rol='EIGENAAR'
        )

        kvk.KvkPersoon.objects.get_or_create(
            prsid=Decimal('300000000000000000'),
            prshibver=Decimal('100000000000000000'),
            faillissement='Nee',
            naam='Testpersoon 2 B.V.',
            persoonsrechtsvorm='BeslotenVennootschap',
            rsin='000000001',
            typering='rechtspersoon',
            uitgebreiderechtsvorm='BeslotenVennootschap',
            verkortenaam='Testpersoon 2 Verkort B.V.',
            volledigenaam='Testpersoon 2 Volledig B.V.',
            rol='EIGENAAR'
        )

        fvv2 = kvk.KvkFunctievervulling.objects.get_or_create(
            ashid=Decimal('100000000000000000'),
            functie="GrandPoobah",
            prsidi=Decimal('200000000000000000'),
            prsidh=Decimal('300000000000000000'),
            soort="OnbeperktBevoegd",
            prsashhibver=Decimal('100000000000000000')
        )[0]

        functievervulling = self._convert(fvv2)

        self.assertIsNotNone(functievervulling)
        self.assertEqual('100000000000000000', functievervulling.id)
        self.assertEqual('GrandPoobah', functievervulling.functietitel)
        self.assertEqual('OnbeperktBevoegd', functievervulling.soortbevoegdheid)
        self.assertEqual(Decimal('300000000000000000'), functievervulling.heeft_aansprakelijke.id)
        self.assertEqual(Decimal('200000000000000000'), functievervulling.is_aansprakelijke.id)

    def test_import_missing_related(self):
        kvk.KvkPersoon.objects.create(
            prsid=Decimal('200000000000000000'),
            prshibver=Decimal('100000000000000000'),
            faillissement='Nee',
            naam='Testpersoon 1 B.V.',
            persoonsrechtsvorm='BeslotenVennootschap',
            rsin='000000001',
            typering='rechtspersoon',
            uitgebreiderechtsvorm='BeslotenVennootschap',
            verkortenaam='Testpersoon Verkort B.V.',
            volledigenaam='Testpersoon Volledig B.V.',
            rol='EIGENAAR'
        )

        fvv1 = kvk.KvkFunctievervulling.objects.create(
            ashid=Decimal('100000000000000000'),
            functie="GrandPoobah",
            prsidi=Decimal('200000000000000000'),
            soort="OnbeperktBevoegd",
            prsashhibver=Decimal('100000000000000000')
        )

        functievervulling = self._convert(fvv1)

        self.assertIsNotNone(functievervulling)
        self.assertEqual(Decimal('200000000000000000'), functievervulling.is_aansprakelijke.id)
