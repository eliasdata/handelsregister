import jsonpickle
from django.contrib.gis.geos import Point
from django.test import TestCase

from datasets import build_hr_data, build_ds_data
from datasets.hr import models
from datasets.hr.tests import factories as hr_factories

point = Point(0.0, 1.1)


class ImportDataselectieTest(TestCase):

    def get_row(self, key):
        r = models.DataSelectie.objects.filter(id=key).get()
        self.assertIsNotNone(r)
        return r

    def test_datasel_import(self):
        hr_factories.create_dataselectie_set()

        build_hr_data.fill_geo_table()

        build_ds_data._build_joined_ds_table()

        # this one is always there
        row = self.get_row('1-1')

        # ??
        jsonapi = jsonpickle.decode(row.api_json)
        self.assertIsInstance(jsonapi, models.DataSelectieView)
