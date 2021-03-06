"""
All commands to create a functioning HR api dataset
"""

import logging

from django.core.management import BaseCommand
from django.conf import settings

# from datasets import build_cbs_sbi

from datasets.sbicodes import load_sbi_codes
from datasets.sbicodes import validate_codes
from datasets import build_ds_data
from datasets import build_hr_data
from datasets.hr import improve_location_with_search
from datasets.hr import handelsregister_stats
from datasets.hr import models

LOG = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Import HR data from handel regster makelaarsuite (mks) dump

    clear data using:

    - manage.py migrate handelsregister zero

    apply new/updated migrations

    - manage.py migrate handelsregister

    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--bagfix',
            action='store_true',
            dest='bag',
            default=False,
            help='Fill hr_locatie with bagnummeraanduiding table')

        parser.add_argument(
            '--geovestigingen',
            action='store_true',
            dest='geo_vest',
            default=False,
            help='Fill hr_geovestigingen table')

        parser.add_argument(
            '--search',
            action='store_true',
            dest='searchapi',
            default=False,
            help='Fill hr_locatie with search api')

        parser.add_argument(
            '--clearsearch',
            action='store_true',
            dest='clearsearch',
            default=False,
            help='Clear hr_locate from search api results')

        parser.add_argument(
            '--testsearch',
            action='store_true',
            dest='testsearch',
            default=False,
            help='Test search algorithm with examples')

        parser.add_argument(
            '--status',
            action='store_true',
            dest='stats',
            default=False,
            help='print location stats')

        parser.add_argument(
            '--cbs_sbi',
            action='store_true',
            dest='cbs_sbi',
            default=False,
            help='Fill cbs sbi-codes')

        parser.add_argument(
            '--cbs_sbi_validate',
            action='store_true',
            dest='cbs_sbi_validate',
            default=False,
            help='Tellingen cbs sbi-codes')

        parser.add_argument(
            '--dataselectie',
            action='store_true',
            dest='dataselectie',
            default=False,
            help='Fill dataselectie view')

        parser.add_argument(
            '--partial',
            action='store',
            dest='partial_index',
            default=0,
            help='Build X/Y parts 1/3, 2/3, 3/3')

        parser.add_argument(
            '--nocache',
            action='store_false',
            dest='use_cache',
            default=True,
            help='save/update json response data in fixtures')

        parser.add_argument(
            '--validate_import',
            action='store_true',
            dest='validate_import',
            default=False,
            help='Validate table counts')

    def handle(self, *args, **options):
        """
        validate and execute import task
        """
        LOG.info('Handelsregister import started')

        set_partial_config(options)

        if options['bag']:
            # copy_bag_to_hr script
            build_hr_data.fill_location_with_bag()
            handelsregister_stats.log_rapport_counts(action='bag')
        elif options['geo_vest']:
            build_hr_data.fill_geo_table()
            handelsregister_stats.log_rapport_counts(action='map')
        elif options['cbs_sbi_validate']:
            # make sure everything has a valid sbi code
            validate_codes.validate()
        elif options['cbs_sbi']:
            use_cache = options['use_cache']
            # load_sbi_codes.build_csb_sbi_code_tree(use_cache=use_cache)
            # load_sbi_codes.build_qa_sbi_code_tree(use_cache=use_cache)
            load_sbi_codes.build_all_sbi_code_trees(use_cache=use_cache)
        elif options['dataselectie']:
            build_ds_data.write_dataselectie_data()
            # handelsregister_stats.log_rapport_counts(action='ds')

        elif options['validate_import']:
            handelsregister_stats.log_rapport_counts(
                action='validate', fail_on_wrong_target=True)
        elif options['searchapi']:
            improve_location_with_search.guess()
            # add extra bag information
            build_hr_data.fill_location_with_bag()
            handelsregister_stats.log_rapport_counts(action='fix')
        elif options['clearsearch']:
            build_hr_data.clear_autocorrect()
        elif options['testsearch']:
            improve_location_with_search.test_bad_examples()
        elif options['stats']:
            handelsregister_stats.log_rapport_counts()
        else:
            # convert mks dump
            build_hr_data.fill_stelselpedia()
            handelsregister_stats.log_rapport_counts(action='mks')
            # now update mks locations with bag locations
            # check if bag data is correctly loaded
            # we need bag data to correct missing geometry data
            build_hr_data.fill_location_with_bag()
            LOG.info('hr_geovestigingen %s', models.Locatie.objects.count())
            assert models.GeoVestigingen.objects.count() == 0
            assert models.Locatie.objects.count() > 200000
            handelsregister_stats.log_rapport_counts(action='bag')


def set_partial_config(options):
    """
    Do partial configuration
    """
    if options['partial_index']:
        numerator, denominator = options['partial_index'].split('/')

        numerator = int(numerator) - 1
        denominator = int(denominator)

        assert (numerator < denominator)
        assert numerator >= 0

        settings.PARTIAL_IMPORT['numerator'] = numerator
        settings.PARTIAL_IMPORT['denominator'] = denominator
