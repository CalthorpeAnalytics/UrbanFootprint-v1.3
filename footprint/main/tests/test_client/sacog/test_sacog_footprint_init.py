from django.core.management import call_command
from django.test.utils import override_settings
from nose import with_setup
from footprint.main.tests.test_client.test_client_footprint_init import TestClientFootprintInit
from footprint import settings

__author__ = 'calthorpe_associates'

class TestScagFootprintInit(TestClientFootprintInit):

    def test_init(self):
        super(TestSacogFootprintInit, self).test_init()
        #raise Exception(settings.CLIENT)
        call_command('footprint_init')
        assert()
