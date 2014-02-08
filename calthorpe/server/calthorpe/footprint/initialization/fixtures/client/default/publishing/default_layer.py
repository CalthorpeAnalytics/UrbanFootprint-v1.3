from footprint.initialization.fixture import LayerConfigurationFixture, ScenarioFixture, RegionFixture, ProjectFixture, GlobalConfigFixture, project_specific_project_fixtures, project_specific_scenario_fixtures
from footprint.initialization.fixtures.client.default.default_mixin import DefaultMixin
from footprint.initialization.publishing.layer_initialization import LayerLibraryKey, LayerMediumKey, LayerSort, LayerTag
from footprint.initialization.publishing.tilestache_style_configuration import create_style_template, create_template_context_dict_for_parent_model
from footprint.initialization.utils import resolve_fixture
from footprint.lib.functions import map_dict_to_dict, dual_map, flat_map, flatten, unique, merge
from footprint.models import BuiltForm, Scenario, Medium
from footprint.models.config.scenario import FutureScenario
from footprint.models.geospatial.feature import Feature
from footprint.models.keys.keys import Keys
from footprint.models.presentation.presentation_configuration import LayerConfiguration, PresentationConfiguration, ConfigurationData
from footprint.utils.range import make_ranges, make_increments
from footprint.models.tag import Tag
import settings

__author__ = 'calthorpe'


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
                name='{0} Default Library', # format with config_entity name
                description='The default layer library for {0}', # format with config_entity name
                data=ConfigurationData(
                    presentation_media_configurations=self.matching_scope(layers or self.layers(),
                                                                          class_scope=self.config_entity.__class__)
                )
            )
        ]

    def all_remote_db_entity_setups(self):
        # Manually coalesce all possible db_entity setups for remote db_entities.
        return unique(
            flat_map(lambda client_instance: client_instance.default_remote_db_entity_setups(),
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
                visible=db_entity_setup['key']=='google_transit',
                tags=[Tag.objects.get(tag=LayerTag.BACKGROUND)],
                sort_priority=LayerSort.BACKGROUND),
            db_entity_setups)

    def layers(self):
        """
            Returns LayerConfigurations that are scoped to a certain LayerLibrary key
        :return:
        """
        return self.background_layers() + [
            # The following layers are Used by both BaseScenario and FutureScenario
            LayerConfiguration(
                scope=FutureScenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_DEVELOPABLE,
                visible=False,
                visible_attributes=['developable_acres'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict=developable_template_context_dict(),
                sort_priority=LayerSort.BASE
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_CENSUS_TRACT,
                visible=False, #Temp
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
                template_context_dict={'attributes': {'blockgroup': {'unstyled': True}}},
                sort_priority=LayerSort.BASE
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_CENSUS_BLOCK,
                visible=False, #Temp
                visible_attributes=['block'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict={'attributes': {'block': {'unstyled': True}}},
                sort_priority=LayerSort.BASE
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_CPAD_HOLDINGS_FEATURE,
                visible=False,
                visible_attributes=['geography_id'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict={'attributes': {'geography_id': {'unstyled': True}}},
                sort_priority=LayerSort.BASE
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,
                visible=False,
                visible_attributes=['builtform_id'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict=built_form_template_context_dict(),
                sort_priority=LayerSort.BASE
            ),
            LayerConfiguration(
                scope=Scenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_BASE_PARCEL_FEATURE,
                visible=False,
                visible_attributes=['builtform_id'],
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
                visible_attributes=['builtform_id'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict=built_form_template_context_dict(),
                sort_priority=LayerSort.FUTURE+1
            ),
            LayerConfiguration(
                scope=FutureScenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_INCREMENT_FEATURE,
                visible=False,
                visible_attributes=['du', 'emp', 'pop'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict={}, #core_increment_template_context_dict()
                sort_priority=LayerSort.FUTURE+3
            ),
            LayerConfiguration(
                scope=FutureScenario.__name__,
                layer_library_key=LayerLibraryKey.DEFAULT,
                db_entity_key=Keys.DB_ABSTRACT_END_STATE_FEATURE,
                visible=False,
                visible_attributes=['builtform_id'],
                tags=[Tag.objects.get(tag=LayerTag.DEFAULT)],
                template_context_dict=built_form_template_context_dict(),
                sort_priority=LayerSort.FUTURE+2
            )
        ]

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
        # Combine unique layers from each project-specific scenario fixture
        layer_configurations = unique(
            flat_map(
                lambda client_scenario: resolve_fixture(
                    "publishing",
                    "layer",
                    LayerConfigurationFixture,
                    client_scenario.schema).layers(),
                project_specific_fixtures),
            lambda layer_configuration: layer_configuration.db_entity_key)

        # Create a default Medium for any layer that doesn't need a Template
        Medium.objects.update_or_create(key=LayerMediumKey.DEFAULT)

        for layer_configuration in layer_configurations:
            if feature_class_lookup.get(layer_configuration.db_entity_key):
                create_style_template(
                    layer_configuration.template_context_dict,
                    layer_configuration.db_entity_key,
                    feature_class_lookup.get(layer_configuration.db_entity_key, None),
                    *layer_configuration.visible_attributes)

        # Creates the Template for LayerSelection instances
        styled_class = Feature
        # This is a magic attribute of tilestache indicating the features that match a query
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
        lambda built_form: built_form.medium.content if built_form.medium else None)


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

    # Creates a dict in the form {
    #   attr1: [ {range: Range(min,max), fill: {color=some_color_of_range}, outline:{outline_color_stuff}},
    #            {range: Range(min,max), fill: {color=another_color_of_range}, outline:{outline_color_stuff}},
    #             ...
    #          ]
    #   attr2: ...
    #}
    # where each attr is one of the class attributes such as du_increments, and each
    # attribute config has an range of values to which a color applies
    # TODO modify to have a cartocss and css version
    return dict(
        htmlClass=None,
        attributes=map_dict_to_dict(
            lambda attr, config: [
                attr,
                dual_map(lambda value_range, color:
                         dict(
                             range=value_range,
                             fill=dict(
                                 # Convert to a hex color string
                                 color='#{0:06x}'.format(color)
                             ),
                             outline={}
                         ),
                         config['values'],
                         config['colors'])
            ],
            dict(
                pop=dict(
                    values=make_ranges(0, 10e6, 5),
                    colors=make_increments(int('0x0', 16), int('0xffffff', 16), 5)
                ),
                du=dict(
                    values=make_ranges(0, 10e6, 5),
                    colors=make_increments(int('0x0', 16), int('0xffffff', 16), 5)
                ),
                emp=dict(
                    values=make_ranges(0, 10e6, 5),
                    colors=make_increments(int('0x0', 16), int('0xffffff', 16), 5)
                )
            )
        ),
    )

