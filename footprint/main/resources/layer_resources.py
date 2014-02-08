# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System. #
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
from tastypie.fields import ToOneField, BooleanField
from footprint.main.models import Layer, LayerLibrary
from footprint.main.resources.mixins.mixins import ToManyFieldWithSubclasses
from footprint.main.resources.presentation_medium_resource import PresentationMediumResource
from footprint.main.resources.presentation_resources import PresentationResource

class LayerLibraryResource(PresentationResource):

    layers = ToManyFieldWithSubclasses(
        'footprint.main.resources.layer_resources.LayerResource',
        attribute='layers',
        full=False,
        null=True)

    class Meta(PresentationResource.Meta):
        resource_name = 'layer_library'
        always_return_data = True
        queryset = LayerLibrary.objects.all()
        excludes = ['presentation_media']

class LayerResource(PresentationMediumResource):

    origin_instance = ToOneField('self', attribute='origin_instance', null=True)
    create_from_selection = BooleanField(attribute='create_from_selection')

    def full_hydrate(self, bundle):
        bundle = super(LayerResource, self).full_hydrate(bundle)
        if bundle.obj.create_from_selection:
            feature_class_configuration = bundle.obj.db_entity_interest.db_entity.feature_class_configuration = bundle.obj.db_entity_interest.db_entity.feature_class_configuration or {}
            feature_class_configuration['source_from_origin_layer_selection'] = True
        return bundle

    class Meta(PresentationMediumResource.Meta):
        resource_name = 'layer'
        always_return_data = True
        queryset = Layer.objects.all()
        filtering = {
            "id": ('exact',),
        }


