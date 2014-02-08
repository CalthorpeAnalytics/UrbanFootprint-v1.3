from footprint.initialization.fixture import LayerConfigurationFixture
from footprint.initialization.fixtures.client.mixins.publishing.layer_primary_base import primary_base_template_context_dict
from footprint.initialization.fixtures.client.scag__irvine.base.scag_general_plan_parcel_feature import ScagGeneralPlanFeature
from footprint.initialization.fixtures.client.scag__irvine.base.scag_existing_land_use_parcel_feature import ScagExistingLandUseParcelFeature
from footprint.models import Project
from footprint.models.config.scenario import BaseScenario, Scenario
from footprint.models.keys.keys import Keys
from footprint.models.presentation.presentation_configuration import LayerConfiguration
from footprint.models.tag import Tag

__author__ = 'calthorpe'


class ScagIrvineLayerConfigurationFixtures(LayerConfigurationFixture):
    def layer_libraries(self, layers=None):

        return self.parent_fixture.layer_libraries(layers or self.layers())

    def layers(self):

        return self.parent_fixture.layers() + [
            LayerConfiguration(
                scope=BaseScenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_SCAG_EXISTING_LAND_USE_PARCEL_SOURCE,
                visible=False,
                visible_attributes=['land_use_definition_id'],
                built_form_set_key='scag_land_use',
                template_context_dict=primary_base_template_context_dict(ScagExistingLandUseParcelFeature)
            ),
            LayerConfiguration(
                scope=BaseScenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_GENERAL_PLAN_FEATURE,
                visible=False,
                visible_attributes=['land_use_definition_id'],
                built_form_set_key='scag_land_use',
                template_context_dict=primary_base_template_context_dict(ScagGeneralPlanFeature)
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
                visible_attributes=['geography_id'],
                template_context_dict={'attributes': {'geography_id': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_SPHERE_OF_INFLUENCE,
                visible=False,
                visible_attributes=['geography_id'],
                template_context_dict={'attributes': {'geography_id': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_FLOODPLAIN,
                visible=False,
                visible_attributes=['geography_id'],
                template_context_dict={'attributes': {'geography_id': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_TIER1_TAZ,
                visible=False,
                visible_attributes=['geography_id'],
                template_context_dict={'attributes': {'geography_id': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_TIER2_TAZ,
                visible=False,
                visible_attributes=['geography_id'],
                template_context_dict={'attributes': {'geography_id': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_TRANSIT_AREAS,
                visible=False,
                visible_attributes=['geography_id'],
                template_context_dict={'attributes': {'geography_id': {'unstyled': True}}}
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                db_entity_key=Keys.DB_ABSTRACT_PARKS_OPEN_SPACE,
                visible=False,
                visible_attributes=['geography_id'],
                template_context_dict={'attributes': {'geography_id': {'unstyled': True}}}
            ),
        ]