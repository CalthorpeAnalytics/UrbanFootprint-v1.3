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

from tastypie import fields
from footprint.main.models.presentation.presentation_configuration import  PresentationConfiguration
from footprint.main.models.presentation.presentation import Presentation
from footprint.main.resources.config_entity_resources import ConfigEntityResource
from footprint.main.resources.mixins.mixins import ToManyFieldWithSubclasses
from footprint.main.resources.pickled_dict_field import PickledObjField
from footprint.main.resources.footprint_resource import FootprintResource

__author__ = 'calthorpe_associates'

class PresentationResource(FootprintResource):

    # Returns instances of the through class, PresentationMedia or subclasses thereof
    presentation_media_query = lambda bundle: bundle.obj.presentationmedium_set.all().select_subclasses()
    presentation_media = ToManyFieldWithSubclasses(
        'footprint.main.resources.presentation_medium_resource.PresentationMediumResource',
        attribute=presentation_media_query,
        full=False,
        null=True)

    # Just return the URI of thie config_entity, since it should always already be loaded by the user beforehand
    config_entity = fields.ToOneField(ConfigEntityResource, 'config_entity', full=False)

    # Only turn on for debugging. This represents the initial configuration of the PresentationMedia, such as visibility
    # configuration = fields.ToOneField('calthorpe.main.resources.presentation_resources.PresentationConfigurationResource', 'configuration', full=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = Presentation.objects.all()



class PresentationConfigurationResource(FootprintResource):
    """
        These are not serialized as part of the API since they represent initial state and all important attributes are copied to the PresentationMedium instances. They can be turned on in PresentationResource for debugging purposes
    """

    data = PickledObjField(attribute='data', readonly=True, null=False, blank=False)

    class Meta(FootprintResource.Meta):
        resource_name = 'presentation_configuration'
        always_return_data = True
        queryset = PresentationConfiguration.objects.all()

