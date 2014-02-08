from django.core.management import call_command
from footprint.initialization.data_provider import DataProvider
from footprint.initialization.fixture import ConfigEntityFixture
from footprint.initialization.utils import resolve_fixture
from footprint.models import Scenario
import settings

__author__ = 'calthorpe'

import unittest

class TestFootprintInit(unittest.TestCase):
    def test_import(self):
        call_command('footprint_init')
        assert(Scenario.objects.count(), DataProvider().scenarios())
