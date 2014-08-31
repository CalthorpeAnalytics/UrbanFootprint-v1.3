# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
# 
# Copyright (C) 2012 Calthorpe Associates
# 
# This program is free software: you can redistribute it and/or modify it under the terms of the
 # GNU General Public License as published by the Free Software Foundation, version 3 of the License.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
# 
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com
from optparse import make_option
from django.core.management.base import BaseCommand
from footprint.main.initialization.data_provider import DataProvider
from footprint.main.models import Layer
from footprint.main.models.application_initialization import application_initialization, update_or_create_config_entities
from footprint.main.models.base.primary_parcel_feature import PrimaryParcelFeature
from footprint.main.models.keys.keys import Keys
from footprint.main.models.presentation.layer_selection import get_or_create_dynamic_layer_selection_class_and_table


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-s', '--skip', action='store_true',  default=False, help='Skip initialization and data creation (for just doing resave)'),
    )

    def handle(self, *args, **options):
        if not options['skip']:
            application_initialization()
            update_or_create_config_entities()

        user = DataProvider().user()['user']
        scenarios = DataProvider().scenarios()
        for scenario in scenarios:
            layer_library = scenario.presentation_set.filter(key=Keys.LAYER_LIBRARY_DEFAULT)[0]
            presentation_medium = layer_library.presentationmedium_set.get(db_entity_key=Keys.DB_ABSTRACT_PRIMARY_PARCEL_SOURCE)
            layer = Layer.objects.get(id=presentation_medium.id) # Cast
            layer_selection_class = get_or_create_dynamic_layer_selection_class_and_table(layer)
            primary_base_feature_class = scenario.feature_class_of_base_class(PrimaryParcelFeature)
            layer_selection = layer_selection_class.objects.get(user=user, layer=layer)
            layer_selection.bounds = primary_base_feature_class.objects.all()[0].geography.geometry
            layer_selection.save()
