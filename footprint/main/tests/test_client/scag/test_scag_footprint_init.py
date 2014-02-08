from django.core.management import call_command
from footprint.main.models import Scenario
from footprint.main.models.keys.keys import Keys
from footprint.main.tests.test_client.test_client_footprint_init import TestClientFootprintInit

__author__ = 'calthorpe_associates'

class TestScagFootprintInit(TestClientFootprintInit):

    def test_init(self):
        super(TestScagFootprintInit, self).test_init()
        #raise Exception(settings.CLIENT)
        call_command('footprint_init')
        assert(Scenario.objects.all()[0].feature_class_of_db_entity_key(Keys.DB_ABSTRACT_PRIMARY_PARCEL_SOURCE).objects.count() > 0)
