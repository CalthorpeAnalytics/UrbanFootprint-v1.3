from footprint.client.configuration.fixture import LayerConfigurationFixture, RegionFixture, GlobalConfigFixture, project_specific_project_fixtures, project_specific_scenario_fixtures
from footprint.client.configuration.default.default_mixin import DefaultMixin
from footprint.main.publishing.layer_initialization import LayerLibraryKey, LayerMediumKey, LayerSort, LayerTag
from footprint.main.publishing.tilestache_style_configuration import create_style_template, create_template_context_dict_for_parent_model
from footprint.client.configuration.utils import resolve_fixture
from footprint.main.lib.functions import flat_map, flatten, unique, merge
from footprint.main.models import BuiltForm, Scenario, Medium, LayerSelection
from footprint.main.models.config.scenario import FutureScenario, BaseScenario
from footprint.main.models.geospatial.feature import Feature
from footprint.main.models.keys.keys import Keys
from footprint.main.models.presentation.presentation_configuration import LayerConfiguration, PresentationConfiguration, ConfigurationData
from footprint.main.models.tag import Tag
from footprint import settings

__author__ = 'calthorpe_associates'


class DefaultLayerConfigurationFixtures(DefaultMixin, LayerConfigurationFixture):
    def layer_libraries(self, layers=None):
        """
           Returns a PresentationConfiguration for each LayerLibrary scoped to self.config_entity.
           The instance will be saved to the LayerLibrary as a foreign key, so it is persisted at that time.
           Each instance contains LayerConfiguration instances that match it's config_entity class scope
        :return:
        """
        # Just make a Scenario scoped configuration
        return [
            PresentationConfiguration(
                # The default LayerLibrary configuration for all scenarios
                scope=self.config_entity.schema(),
                key=LayerLibraryKey.DEFAULT,
                name='{0} Default Library',  # format with config_entity name
                description='The default layer library for {0}',  # format with config_entity name
                data=ConfigurationData(
                    presentation_media_configurations=self.matching_scope(layers or self.layers(),
                                                                          class_scope=self.config_entity and self.config_entity.__class__)
                )
            )
        ]

    def all_remote_db_entity_setups(self):
        # Manually coalesce all possible db_entity setups for remote db_entities.
        return unique(
            flat_map(lambda client_instance: client_instance.default_remote_db_entity_configurations(),
                     flatten([
                         [resolve_fixture("config_entity", "global_config", GlobalConfigFixture, settings.CLIENT)],
                         # Assume only one region matching the CLIENT string
                         [resolve_fixture("config_entity", "region", RegionFixture, settings.CLIENT)],
                         # Iterate through all project-specific project configs
                         project_specific_project_fixtures(),
                         # Iterate through all project-specific scenario configs
                         project_specific_scenario_fixtures()
                     ])),
            lambda db_entity_setup: db_entity_setup['key'])

    def background_layers(self):
        """
            Background layers are simple references to their corresponding db_entities. For now we assume any
            db_entity that has a url is a background layer.
        :return:
        """
        # Find all unique db_entity setups that have the url property
        db_entity_setups = filter(
            lambda db_entity_setup: db_entity_setup.get('url', None),
            self.all_remote_db_entity_setups())
        return map(
            lambda db_entity_setup: LayerConfiguration(
                scope=Scenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=db_entity_setup['key'],
                visible=db_entity_setup['key']=='google_map',
                tags=[Tag.objects.get(tag=LayerTag.BACKGROUND_IMAGERY)],
                sort_priority=LayerSort.BACKGROUND),
            db_entity_setups)

    def layers(self):
        """
            Returns LayerConfigurations that are scoped to a certain LayerLibrary key
        :return:
        """

        return self.matching_scope(self.background_layers() + [
            # The following layers are Used by both BaseScenario and FutureScenario
            LayerConfiguration(
                scope=FutureScenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_DEVELOPABLE,
                visible=False,
                visible_attributes=['developable_index'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict={'attributes': {'developable_index': {'unstyled': True}}},
                sort_priority=LayerSort.BASE
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_CENSUS_TRACT,
                visible=False,
                # TODO why style tract codes?
                visible_attributes=['tract'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict={'attributes': {'tract': {'unstyled': True}}},
                sort_priority=LayerSort.BASE
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_CENSUS_BLOCKGROUP,
                visible=False, #Temp
                visible_attributes=['blockgroup'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                # TODO why style blockgroup codes?
                template_context_dict={'attributes': {'blockgroup': {'unstyled': True}}},
                sort_priority=LayerSort.BASE
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_CENSUS_BLOCK,
                visible=False,
                visible_attributes=['block'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                # TODO why style block codes?
                template_context_dict={'attributes': {'block': {'unstyled': True}}},
                sort_priority=LayerSort.BASE
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_CPAD_HOLDINGS_FEATURE,
                visible=False,
                visible_attributes=['wkb_geometry'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}},
                sort_priority=LayerSort.BASE
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,
                visible=False,
                visible_attributes=['built_form__id'],
                column_alias_lookup=dict(built_form__id='built_form_id'),
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict=built_form_template_context_dict(),
                sort_priority=LayerSort.BASE
            ),

            # The following are only used by FutureScenario
            LayerConfiguration(
                scope=FutureScenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_FUTURE_SCENARIO_FEATURE,
                visible=True,
                visible_attributes=['built_form__id'],
                # The SQL column returned is normally builform_id, so alias it to our expected attribute string
                column_alias_lookup=dict(built_form__id='built_form_id'),
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict=built_form_template_context_dict(),
                sort_priority=LayerSort.FUTURE+1
            ),
            LayerConfiguration(
                scope=FutureScenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_INCREMENT_FEATURE,
                visible=False,
                visible_attributes=['land_development_category'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict={'attributes': {'land_development_category': {'unstyled': True}}},
                sort_priority=LayerSort.FUTURE+3
            ),

            LayerConfiguration(
                scope=FutureScenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_END_STATE_FEATURE,
                visible=False,
                visible_attributes=['built_form__id'],
                column_alias_lookup=dict(built_form__id='built_form_id'),
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict=built_form_template_context_dict(),
                sort_priority=LayerSort.FUTURE+2
            ),

            LayerConfiguration(
                scope=Scenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_VMT_FEATURE,
                visible=False,
                visible_attributes=['vmt_daily_per_hh'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict={'attributes': {'vmt_daily_per_hh': {'unstyled': True}}},
                sort_priority=LayerSort.FUTURE+4
            )
        ], class_scope=self.config_entity and self.config_entity.__class__)

    def import_layer_configurations(self):
        """
            Generic LayerConfigurations for db_entity layers imported into the system.
        """
        return self.matching_scope([
            LayerConfiguration(
                scope=FutureScenario.__name__,
                # Use Feature for the template key so we match the default Feature
                # style files
                style_class=Feature,
                layer_library_key=LayerLibraryKey.DEFAULT,
                visible=True,
                visible_attributes=['wkb_geometry'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}},
                sort_priority=LayerSort.FUTURE,
                # This is meant to be replaced by the imported db_entity_key
                # It serves to uniquely identify the LayerConfiguration
                # so that it can be overridden by client configurations
                db_entity_key='default_future_scenario_layer_configuration'
            ),
            LayerConfiguration(
                scope=BaseScenario.__name__,
                # Use Feature for the template key so we match the default Feature
                # style files
                style_class=Feature,
                layer_library_key=LayerLibraryKey.DEFAULT,
                visible=True,
                visible_attributes=['wkb_geometry'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict={'attributes': {'wkb_geometry': {'unstyled': True}}},
                sort_priority=LayerSort.BASE,
                # This is meant to be replaced by the imported db_entity_key
                # It serves to uniquely identify the LayerConfiguration
                # so that it can be overridden by client configurations
                db_entity_key='default_base_scenario_layer_configuration'
            )
        ], class_scope=self.config_entity and self.config_entity.__class__)

    def update_or_create_media(self):
        """
            Iterates through the LayerConfiguration and creates Template instances for each that contain default
            styling for the configured attributes
        :return:
        """

        # Use the client_scenario to get all the DbEntity key to FeatureClass mappings, since the Scenario will adopt
        # from its ancestors
        # Find any project_specific scenario_fixtures
        project_specific_fixtures = project_specific_project_fixtures()
        # Merge feature_class_lookups from each project-specific scenario fixture
        feature_class_lookup = merge(
            *map(
                lambda client_scenario: client_scenario.feature_class_lookup(),
                project_specific_scenario_fixtures()))
        # Combine unique layer configurations from each project-specific scenario fixture
        # Also add in import layer configurations to support imported layers
        def layer_configurations_for_client_scenario(client_scenario):
            client_fixture = resolve_fixture(
                "publishing",
                "layer",
                LayerConfigurationFixture,
                client_scenario.schema)
            return client_fixture.layers() + client_fixture.import_layer_configurations()

        # Get a flat unique list of layer configurations for all client scenario fixtures
        layer_configurations = unique(
            flat_map(
                layer_configurations_for_client_scenario,
                project_specific_fixtures),
            lambda layer_configuration: layer_configuration.db_entity_key)

        # Create a default Medium for any layer that doesn't need a Template
        Medium.objects.update_or_create(key=LayerMediumKey.DEFAULT)

        for layer_configuration in layer_configurations:
            if layer_configuration.style_class or feature_class_lookup.get(layer_configuration.db_entity_key):
                create_style_template(
                    layer_configuration.template_context_dict,
                    layer_configuration.db_entity_key,
                    # The template key is based on the configured feature class or the DbEntity
                    # If no feature_class exists the db_entity_key is used
                    # Some layer configurations use styled_class to force a certain class upon
                    # which to base their template names (namely the generic layer_configurations)
                    # used for importing new feature tables
                    layer_configuration.style_class or feature_class_lookup.get(layer_configuration.db_entity_key),
                    *layer_configuration.visible_attributes)

        # Creates the Template for LayerSelection instances
        styled_class = LayerSelection
        # This is a magic attribute of tilestache indicating the features that match a query
        # TODO we don't style layer selections with cartocss.
        # Is this being used on the front end with css/polymaps?
        styled_attribute = 'selected'
        default_context = {
            'htmlClass': None,
            'attributes': {
                styled_attribute: {
                    'equals': {
                        'TRUE': {"fill": {"color": 'yellow', "opacity": .8},
                                 "outline": {"color": "red"}, },
                    },
                }
            }
        }
        create_style_template(default_context, None, styled_class, styled_attribute)


def built_form_template_context_dict():
    """
        Create the template_context_dict based on the built_form_id attribute
    :return:
    """

    return create_template_context_dict_for_parent_model(
        BuiltForm,
        lambda built_form: built_form.medium.content if built_form.medium else None,
        'built_form')


def developable_template_context_dict():
    """
        Create the template_context_dict for the DevelopableFeature class
        TODO fill this out
    :return:
    """
    return dict()


def core_increment_template_context_dict():
    """
        Initialize the Template for the CoreIncrementFeatures class attributes.
        This creates a context of default feature value ranges and colors for each attribute that are copied to the
        PresentationMedium.medium_context for each Scenario map presentation. The user can then update the colors
        and values in the UI
    :return:
    """
    return dict()

