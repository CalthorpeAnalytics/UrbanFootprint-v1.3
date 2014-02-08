from django.core.management import call_command
from footprint.models import Scenario
from footprint.models.keys.keys import Keys
from footprint.tests.test_client.test_client_footprint_init import TestClientFootprintInit

__author__ = 'calthorpe'

class TestScagFootprintInit(TestClientFootprintInit):

    def test_init(self):
        super(TestScagFootprintInit, self).test_init()
        #raise Exception(settings.CLIENT)
        call_command('footprint_init')
        assert(Scenario.objects.all()[0].feature_class_of_db_entity(Keys.DB_ABSTRACT_PRIMARY_PARCEL_SOURCE).objects.count() > 0)
