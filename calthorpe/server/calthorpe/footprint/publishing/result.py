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
from footprint.initialization.fixture import ResultConfigurationFixture
from footprint.initialization.utils import resolve_fixture
from footprint.lib.functions import map_to_dict
from footprint.models import DbEntityInterest
from footprint.models.config.scenario import Scenario
from footprint.models.presentation.result_library import ResultLibrary
from footprint.models.presentation.result import Result

__author__ = 'calthorpe'

def update_or_create_result_libraries(config_entity):
    """
        Creates a ResultLibrary and its Result instances upon saving a config_entity if they do not yet exist.
    :param config_entity
    :return:
    """

    # TODO, there's a problem of Region and Project presentations overwriting the association rows of other ConfigEntities
    # Just process Scenarios
    if not isinstance(config_entity, Scenario):
        return

    client_result = resolve_fixture(
        "publishing",
        "result",
        ResultConfigurationFixture,
        config_entity.schema(),
        config_entity=config_entity)

    # Create each ResultLibrary and store them as a dict keyed by their key
    result_library_lookup = map_to_dict(lambda result_library_config: [
        result_library_config.key,
        ResultLibrary.objects.update_or_create(
            key=result_library_config.key,
            config_entity=config_entity,
            scope=config_entity.schema(),
            defaults=dict(
                name=result_library_config.name.format(config_entity.name),
                description=result_library_config.description.format(config_entity.name)
            )
        )[0]],
        client_result.result_libraries())

    # Create each configured Result
    for result_config in client_result.results():

        # Create the db_entity and db_entity_interest for the result
        db_entity_setup = dict(db_entity=result_config.update_or_create_db_entity(config_entity))
        # Add it to the config_entity
        config_entity.sync_db_entities(db_entity_setup)
        # Test the query
        db_entity_setup['db_entity'].parse_query(config_entity)

        # Create a result for each result key given.
        Result.objects.update_or_create(
            # Match the Result to the right ResultLibrary
            presentation=result_library_lookup[result_config.result_library_key],
            db_entity_key=result_config.result_db_entity_key,
            defaults=dict(
                # Use the Result's custom Medium, keyed by the Result key
                medium=result_config.resolve_result_medium(),
                configuration=result_config.get_presentation_medium_configuration())
        )
    # Remove orphan results and their DbEntityInterests/DbEntities
    result_library_ids = map(lambda result_library: result_library.id, ResultLibrary.objects.filter(config_entity=config_entity))
    valid_result_keys = map(lambda result_config: result_config.result_db_entity_key, client_result.results())
    orphan_results = Result.objects.filter(presentation__id__in=result_library_ids).exclude(db_entity_key__in=valid_result_keys)
    DbEntityInterest.objects.filter(config_entity=config_entity, db_entity__key__in=map(lambda result: result.db_entity_key, orphan_results)).delete()
    orphan_results.delete()

def on_config_entity_post_save_result(sender, **kwargs):
    """
        Sync a ConfigEntity's ResultPage presentation
    """
    config_entity = kwargs['instance']
    update_or_create_result_libraries(config_entity)

def on_db_entity_save():
    """
    respond to whenever a db entity is added or updated
    :return:
    """
    pass

def on_layer_style_save():
    """
    respond to any changes in style (
    :return:
    """
    pass


def on_config_entity_post_save(sender, **kwargs):
    """
        Sync tilestache to a ConfigEntity class after the latter is saved
    """
    config_entity = kwargs['instance']


def on_config_entity_pre_delete_results(sender, **kwargs):
    """
        Sync geoserver to a ConfigEntity class after the latter is saved
    """
    config_entity = kwargs['instance']


