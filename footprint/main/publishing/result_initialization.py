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
from django.dispatch import receiver
from inflection import titleize
from footprint.main.models.geospatial.feature_behavior import FeatureBehavior
from footprint.main.models.geospatial.db_entity import DbEntity
from footprint.main.models.geospatial.behavior import BehaviorKey, Behavior
from footprint.main.models.geospatial.feature_class_configuration import FeatureClassConfiguration
from footprint.main.models.signals import initialize_media
from footprint.main.lib.functions import dual_map_to_dict, map_to_dict, get_first, filter_keys, merge
from footprint.main.models.presentation.medium import Medium
from footprint.main.models.keys.keys import Keys
from footprint.main.utils.utils import expect, resolvable_model_name
from footprint import settings

__author__ = 'calthorpe_associates'

@receiver(initialize_media)
def initialize_result_media(sender, **kwargs):
    """
        This fires when the application initializes or updates. It creates style templates and their default contexts
        for the results
    :param sender:
    :param kwargs:
    :return:
    """
    from footprint.client.configuration.fixture import ResultConfigurationFixture
    from footprint.client.configuration.utils import resolve_fixture

    client_result = resolve_fixture(
        "publishing",
        "result",
        ResultConfigurationFixture,
        settings.CLIENT)
    client_result.update_or_create_media()

class ResultLibraryKey(Keys):
    class Fab(Keys.Fab):
        @classmethod
        def prefix(cls):
            return 'result_library'

    # The default result library
    DEFAULT = Fab.ricate('default')

class ResultKey(Keys):
    class Fab(Keys.Fab):
        @classmethod
        def prefix(cls):
            return 'result'
    BASE_EMPLOYMENT_BY_TYPE = Fab.ricate('base_employment_by_type')
    BASE_DWELLING_UNITS_BY_TYPE = Fab.ricate('base_dwelling_units_by_type')
    INCREMENTS = Fab.ricate('increments')
    INCREMENTS_EMPLOYMENT_BY_TYPE = Fab.ricate('increments_employment_by_type')
    INCREMENTS_DWELLING_UNITS_BY_TYPE = Fab.ricate('increments_dwelling_units_by_type')
    INCREMENTS_BARS = Fab.ricate('increments_bars')
    END_STATE = Fab.ricate('end_state')
    END_STATE_EMPLOYMENT_BY_TYPE = Fab.ricate('end_state_employment_by_type')
    END_STATE_DWELLING_UNITS_BY_TYPE = Fab.ricate('end_state_dwelling_units_by_type')
    END_STATE_BARS = Fab.ricate('end_state_bars')
    FISCAL = Fab.ricate('fiscal')
    VMT = Fab.ricate('vmt')
    ENERGY = Fab.ricate('energy')
    WATER = Fab.ricate('water')
    AGRICULTURE = Fab.ricate('agriculture')


class ResultMediumKey(ResultKey):
    class Fab(Keys.Fab):
        @classmethod
        def prefix(cls):
            return 'result__medium'

    # The default medium for all results
    DEFAULT = Fab.ricate('default')
    BASE_EMPLOYMENT_BY_TYPE = Fab.ricate('base_employment_by_type')
    BASE_DWELLING_UNITS_BY_TYPE = Fab.ricate('base_dwelling_units_by_type')
    INCREMENTS = Fab.ricate('increments')
    INCREMENTS_DWELLING_UNITS_BY_TYPE = Fab.ricate('increments_dwelling_units_by_type')
    INCREMENTS_EMPLOYMENT_BY_TYPE = Fab.ricate('increments_employment_by_type')
    END_STATE = Fab.ricate('end_state')
    END_STATE_EMPLOYMENT_BY_TYPE = Fab.ricate('end_state_employment_by_type')
    END_STATE_DWELLING_UNITS_BY_TYPE = Fab.ricate('end_state_dwelling_units_by_type')
    END_STATE_BARS = Fab.ricate('end_state_bars')


class ResultLibraryConfiguration(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        expect(self, 'key', 'name', 'description')
        # The optional ConfigEntity class scope of the Result. Only config_entities that match or inherit this will create a result_library
    class_scope=None,
    key=None,
    name=None,
    description=None

class ResultConfiguration(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    # The optional ConfigEntity class scope of the Result. Only config_entities that match or inherit this will create a result
    class_scope = None
    # The key of the ResultLibrary to which this Result belongs
    # This could be refactored to allow multiple libraries
    result_library_key = None
    # The result type 'bar_graph', 'analytic_bars'
    result_type = None
    # The key of the created DbEntity for the Result. These must be unique across a config_entity
    result_db_entity_key = None,
    name = None,
    # The class attributes to show in the result. These are used for column names, data, control totals, etc.
    attributes = [],
    # Localized and presentable name for attributes, by matching array order
    labels = [],
    # A dict mapping each attribute to the database column name returned by the query, without the __sum, __avg, etc suffix
    db_column_lookup = {},
    # Maps each attribute to a dict with a min and max to use for extents for result presentations that need them static
    extent_lookup = {},
    # Is the bar graph stackable
    stackable = False,
    # Is the bar graph stacked initially
    is_stacked = False,
    # Indicates that control total lines should be drawn on the graph
    include_control_totals = True
    # The source DbEntity from which the Result's DbEntity is cloned
    source_db_entity_key = None
    # Query lambda for the Result
    create_query = None

    def get_presentation_medium_configuration(self):
        """
            Extracts the essential information needed by the Result configuration attribute
        :return:
        """
        return dict(
            # Create a dict that translates the column names to labels
            column_to_label=self.create_column_to_label(),
            # Create a dict that translates the column names to attribute names (used by the UI)
            attribute_to_column=self.db_column_lookup,
            # fixes attribute order
            attributes=self.attributes,
            extent_lookup=self.extent_lookup,
            stackable=self.stackable,
            is_stacked=self.is_stacked,
            result_type=self.result_type,
            # Set a control total to 0 for each column
            control_totals=self.create_control_totals() if self.include_control_totals else [],
            sort_priority=self.sort_priority
        )

    def update_or_create_db_entity(self, config_entity):
        """
            Clone the DbEntity from the increments DbEntity
            This means the queryset is run on the Increments class manager

        :param config_entity:
        :return: Return the DbEntity
        """

        # The Behavior keyspace
        behavior_key = BehaviorKey.Fab.ricate
        # Used to load Behaviors defined elsewhere
        get_behavior = lambda key: Behavior.objects.get(key=behavior_key(key))
        return self.clone_db_entity_and_interest_for_result(
            config_entity,
            self.source_db_entity_key,
            #TODO redo this whole flow in the new configuration style
            key=self.result_db_entity_key,
            name=titleize(self.result_db_entity_key),
            query=self.create_query(self),
            feature_behavior=FeatureBehavior(
                behavior=get_behavior('result')
            )
        ).db_entity

    def clone_db_entity_and_interest_for_result(self, config_entity, reference_db_entity_key, **kwargs):
        """
            Clone the selected db_entity of key reference_db_entity and replace any of its attributes with those
            specified in **kwargs. **kwargs should contain a unique key property
        :param reference_db_entity_key: key of the DbEntity to clone
        :param kwargs: replacement values containing at the very least 'key'
        :return: The DbEntityInterest which references the cloned db_entity
        """
        source_db_entity = config_entity.computed_db_entities().get(key=reference_db_entity_key)
        # Avoid circular reference
        from footprint.main.publishing.db_entity_publishing import clone_or_update_db_entity_and_interest

        return clone_or_update_db_entity_and_interest(
            config_entity,
            source_db_entity,
            DbEntity(**merge(
                kwargs,
                dict(
                    feature_class_configuration=FeatureClassConfiguration(
                        **merge(source_db_entity.feature_class_configuration.__dict__,
                                dict(feature_class_owner=reference_db_entity_key))),
                )
            )),
            override_on_update=True
        )

    def create_column_to_label(self):
        """
            Create a mapping between table column names and labels, based on the attribute names
        :return:
        """
        return dual_map_to_dict(
            lambda attribute, label: [self.db_column_lookup[attribute], label],
            self.attributes,
            self.labels)

    def create_control_totals(self):
        """
            Create a dict of initial control totals
        :return:
        """
        return map_to_dict(
            lambda column: [column, 0],
            self.attributes)

    def resolve_result_medium(self):
        """
            Get the Medium of the result key or default
        :return:
        """
        return get_first(
            # See if a Medium exists with a key corresponding to the result
            # Default to the default Medium for results
            Medium.objects.filter(key=self.result_db_entity_key.replace('result', 'result__medium')),
            Medium.objects.get(key=ResultMediumKey.DEFAULT)
        )
class ResultSort(object):
    FUTURE = 10
    BASE = 20
    OTHER = 60
    BACKGROUND = 80
