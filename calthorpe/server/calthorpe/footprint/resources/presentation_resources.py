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
from tastypie.fields import CharField, DictField, ListField
from footprint.models import PresentationConfiguration, ResultLibrary, LayerLibrary, PresentationMedium
from footprint.models.presentation.result import Result
from footprint.models.presentation.presentation import Presentation
from footprint.resources.config_entity_resources import ConfigEntityResource
from footprint.resources.db_entity_resources import DbEntityInterestResource
from footprint.resources.medium_resources import MediumResource
from footprint.resources.mixins.mixins import ToManyFieldWithSubclasses, TagResourceMixin
from footprint.resources.pickled_dict_field import PickledDictField, PickledObjField
from footprint.resources.footprint_resource import FootprintResource

__author__ = 'calthorpe'

class PresentationResource(FootprintResource):

    # Returns instances of the through class, PresentationMedia or subclasses thereof
    presentation_media_query = lambda bundle: bundle.obj.presentationmedium_set.select_subclasses()
    presentation_media = ToManyFieldWithSubclasses(
        'footprint.resources.presentation_resources.PresentationMediumResource',
        attribute=presentation_media_query,
        full=True,
        null=True)

    # Just return the URI of thie config_entity, since it should always already be loaded by the user beforehand
    config_entity = fields.ToOneField(ConfigEntityResource, 'config_entity', full=False)

    # Only turn on for debugging. This represents the initial configuration of the PresentationMedia, such as visibility
    # configuration = fields.ToOneField('footprint.resources.presentation_resources.PresentationConfigurationResource', 'configuration', full=True)

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = Presentation.objects.all()


class PresentationMediumResource(FootprintResource, TagResourceMixin):
    """
        The through class between Presentation and Medium, a list of which are loaded by a PresentationResource instance to give the user access to the corresponding Medium and also the important db_entity method, which returns the selected DbEntity interest of the PresentationMedium's db_entity_key
    """

    # A readonly attribute derived from the db_entity_key
    db_entity_interest = fields.ToOneField(DbEntityInterestResource, attribute='db_entity_interest', full=True, null=True)

    # Just return the uri to the Presentation, assuming we loaded this resource instance in the context of a Presentation
    presentation = fields.ToOneField(PresentationResource, attribute='presentation', null=False, full=False)
    # Return the full Medium
    medium = fields.ToOneField(MediumResource, attribute='medium', null=False, full=True)

    # The currently configured context dict for the medium. These are generally the values edited by the user in the UI
    medium_context = PickledDictField(attribute='medium_context', null=True, blank=True, default=lambda:{'test':True})

    # The configuration of items not directly related to the Medium, such as graph labels. These are usually also
    # editable by the user
    configuration = PickledDictField(attribute='configuration', null=True, blank=True, default=lambda:{'test':True})

    visible_attributes = ListField(attribute='visible_attributes', null=True, blank=True)

    # The rendered version of the Medium that is rendered based on the current medium_context values and teh
    # configuration values
    # This might be CSS, a dict of multiple CSS, or anything else that needs to be rendered on the server but
    # shown in the browser
    rendered_medium = CharField(attribute='rendered_medium', null=True, blank=True)

    class Meta(FootprintResource.Meta):
        resource_name = 'presentation_medium'
        always_return_data = True
        queryset = PresentationMedium.objects.all()


class PresentationConfigurationResource(FootprintResource):
    """
        These are not serialized as part of the API since they represent initial state and all important attributes are copied to the PresentationMedium instances. They can be turned on in PresentationResource for debugging purposes
    """

    data = PickledObjField(attribute='data', readonly=True, null=False, blank=False)

    class Meta(FootprintResource.Meta):
        resource_name = 'presentation_configuration'
        always_return_data = True
        queryset = PresentationConfiguration.objects.all()

