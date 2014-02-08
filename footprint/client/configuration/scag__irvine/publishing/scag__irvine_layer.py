from footprint.client.configuration.fixture import LayerConfigurationFixture
from footprint.client.configuration.mixins.publishing.layer_primary_base import primary_base_template_context_dict
from footprint.client.configuration.scag__irvine.base.scag_general_plan_parcel_feature import ScagGeneralPlanParcelFeature
from footprint.client.configuration.scag__irvine.base.scag_existing_land_use_parcel_feature import ScagExistingLandUseParcelFeature
from footprint.main.models.config.scenario import BaseScenario, Scenario
from footprint.main.models.keys.keys import Keys
from footprint.main.models.presentation.presentation_configuration import LayerConfiguration

__author__ = 'calthorpe_associates'


class ScagIrvineLayerConfigurationFixtures(LayerConfigurationFixture):
    def layer_libraries(self, layers=None):

        return self.parent_fixture.layer_libraries(layers or self.layers())

    def layers(self):

        return self.parent_fixture.layers() + [
            LayerConfiguration(
                scope=BaseScenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_SCAG_EXISTING_LAND_USE_PARCEL_SOURCE,
                visible=False,
                visible_attributes=['land_use_definition__id'],
                column_alias_lookup=dict(land_use_definition__id='land_use_defintion_id'),
                #built_form_set_key='scag_land_use',
                template_context_dict=primary_base_template_context_dict(ScagExistingLandUseParcelFeature)
            ),
            LayerConfiguration(
                scope=BaseScenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_GENERAL_PLAN_FEATURE,
                visible=False,
                visible_attributes=['land_use_definition__id'],
                column_alias_lookup=dict(land_use_definition__id='land_use_defintion_id'),
                #built_form_set_key='scag_land_use',
                template_context_dict=primary_base_template_context_dict(ScagGeneralPlanParcelFeature)
            ),
            LayerConfiguration(
                scope=BaseScenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_PRIMARY_SPZ_SOURCE,
                visible=True,
                visible_attributes=['spzid'],
                template_context_dict={'attributes': {'spzid': {'unstyled': True}}}
            ),
            # The following are scoped for both Scenario subclasses
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_JURISDICTION_BOUNDARY,
                visible=True,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_SPHERE_OF_INFLUENCE,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_FLOODPLAIN,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_TIER1_TAZ,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_TIER2_TAZ,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_PARKS_OPEN_SPACE,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_TRANSIT_AREAS,
                visible=False,
                visible_attributes=['wkb_geometry'],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}}
            ),
        ]

    def import_layer_configurations(self):
        return self.parent_fixture.import_layer_configurations()
