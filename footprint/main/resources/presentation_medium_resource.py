from tastypie import fields
from tastypie.fields import ListField, CharField
from footprint.main.lib.functions import remove_keys
from footprint.main.models import PresentationMedium
from footprint.main.resources.db_entity_resources import DbEntityInterestResource
from footprint.main.resources.footprint_resource import FootprintResource
from footprint.main.resources.medium_resources import MediumResource
from footprint.main.resources.mixins.mixins import TagResourceMixin
from footprint.main.resources.pickled_dict_field import PickledDictField
from footprint.main.resources.presentation_resources import PresentationResource

__author__ = 'calthorpe'

class PresentationMediumResource(FootprintResource, TagResourceMixin):
    """
        The through class between Presentation and Medium, a list of which are loaded by a PresentationResource instance to give the user access to the corresponding Medium and also the important db_entity method, which returns the selected DbEntity interest of the PresentationMedium's db_entity_key
    """

    # The DbEntityInterest of the layer.
    # This must be created when the layer is created
    # DbEntityInterest is actually accessed through a getter/setter on the presentation_medium
    # Since it belongs to the presentation.config_entity.
    db_entity_interest = fields.ToOneField(DbEntityInterestResource, attribute='db_entity_interest', full=True, null=False)

    # The db_entity_key set by the db_entity_interest--update/create goes through db_entity_interest
    db_entity_key = fields.CharField(attribute='db_entity_key', null=False)
    def hydrate_db_entity_key(self, bundle):
        if bundle.data['db_entity_interest']:
            bundle.data['db_entity_key'] = bundle.data['db_entity_interest']['db_entity']['key']
        return bundle

    # Just return the uri to the Presentation, assuming we loaded this resource instance in the context of a Presentation
    presentation = fields.ToOneField(PresentationResource, attribute='presentation', null=False, full=False)

    # Return the full Medium
    medium = fields.ToOneField(MediumResource, attribute='medium', null=False, full=True)
    # The currently configured context dict for the medium. These are generally the values edited by the user in the UI
    medium_context = PickledDictField(attribute='medium_context', null=True, blank=True, default=lambda: {})
    # The configuration of items not directly related to the Medium, such as graph labels. These are usually also
    # editable by the user
    configuration = PickledDictField(attribute='configuration', null=True, blank=True, default=lambda: {})

    visible_attributes = ListField(attribute='visible_attributes', null=True, blank=True)

    # The rendered version of the Medium that is rendered based on the current medium_context values and the
    # configuration values
    # This might be CSS, a dict of multiple CSS, or anything else that needs to be rendered on the server but
    # shown in the browser
    rendered_medium = CharField(attribute='rendered_medium', null=True, blank=True)

    def hydrate(self, bundle):
        return super(PresentationMediumResource, self).hydrate(bundle)

    def dehydrate(self, bundle):
        return super(PresentationMediumResource, self).dehydrate(bundle)

    def dehydrate_medium_context(self, bundle):
        # Remove data that isn't needed by the API
        return remove_keys(bundle.data['medium_context'], ['attributes'])

    class Meta(FootprintResource.Meta):
        resource_name = 'presentation_medium'
        always_return_data = True
        queryset = PresentationMedium.objects.all()
        excludes = ['rendered_medium']

