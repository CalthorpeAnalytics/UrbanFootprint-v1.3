from django.core.management import call_command
from footprint.main.initialization.data_provider import DataProvider
from footprint.main.models import Scenario

__author__ = 'calthorpe_associates'

import unittest

class TestFootprintInit(unittest.TestCase):
    def test_import(self):
        call_command('footprint_init')
        assert(Scenario.objects.count(), DataProvider().scenarios())
