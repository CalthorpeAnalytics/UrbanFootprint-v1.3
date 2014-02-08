# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
import os
from django.core.management import call_command
from django.conf import settings

from footprint.client.configuration.fixture import InitFixture
from footprint.client.configuration.sacog.built_form.sacog_land_use_definition import SacogLandUseDefinition

class SacogInitFixture(InitFixture):
    def model_class_modules(self):
        """
        SACOG defines additional concrete model classes in the following modules
        :return:
        """
        return [
            ("built_form", "land_use_definition"),
            ("built_form", "land_use")
        ]

    def import_database(self):
        if settings.USE_SAMPLE_DATA_SETS and settings.USE_LOCAL_SAMPLE_DATA_SETS:
            dct = settings.DATABASES['sample_data']
            return dict(
                host=dct['HOST'],
                database=dct['NAME'],
                user=dct['USER'],
                password=dct['PASSWORD']
            )
        else:
            return dict(
                host='10.0.0.133',
                database='sacog_urbanfootprint',
                user='calthorpe',
                password='[PASSWORD]'
            )

    def populate_models(self):
        if SacogLandUseDefinition.objects.count() == 0:
            print "loading sacog land uses"
            fixture_path = os.path.join(settings.SERVER_ROOT, 'footprint', 'client', 'configuration',
                            'sacog', 'built_form', 'sacog_land_use_definitions.json')
            call_command('loaddata', fixture_path)
        else:
            print "skipping because of " + str(SacogLandUseDefinition.objects.count()) + " objects already there"

    def users(self):
        return [
            dict(username='test', password='test', email='testy@test.ca', api_key='TEST_API_KEY'),
            dict(username='raef', password='raef', email='raef@sacog.gov'),
            dict(username='jennifer', password='test', email='jennifer@test.ca', api_key='TEST_API_KEY'),
        ]
