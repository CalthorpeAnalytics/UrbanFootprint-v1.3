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
# from memory_profiler import profile
import logging
from footprint.client.configuration.fixture import ResultConfigurationFixture
from footprint.client.configuration.utils import resolve_fixture
from footprint.main.lib.functions import map_to_dict
from footprint.main.models.config.config_entity import ConfigEntity
from footprint.main.models.config.db_entity_interest import DbEntityInterest

from footprint.main.models.config.scenario import Scenario
from footprint.main.models.presentation.result_library import ResultLibrary
from footprint.main.models.presentation.result import Result

logger = logging.getLogger(__name__)

__author__ = 'calthorpe_associates'

#@profile
def on_config_entity_post_save_result(sender, **kwargs):
    """
        Sync a ConfigEntity's ResultPage presentation
        :param kwargs: 'db_entity_keys' Optional list to limit which DbEntities are processed
    """
    config_entity = kwargs['instance']
    logger.debug("\t\tHandler: on_config_entity_post_save_result. ConfigEntity: %s" % config_entity.name)
    if ConfigEntity._heapy:
        ConfigEntity.dump_heapy()
    update_or_create_result_libraries(config_entity)

#@profile
def on_db_entity_post_save_result(sender, **kwargs):
    db_entity_interest = kwargs['instance']
    config_entity = db_entity_interest.config_entity
    db_entity = db_entity_interest.db_entity
    logger.debug("\t\tHandler: on_db_entity_post_save_layer. DbEntity: %s" % db_entity.full_name)
    if ConfigEntity._heapy:
        ConfigEntity.dump_heapy()
    update_or_create_result_libraries(config_entity, db_entity_keys=[db_entity.key])

def update_or_create_result_libraries(config_entity, **kwargs):
    """
        Creates a ResultLibrary and its Result instances upon saving a config_entity if they do not yet exist.
        :param config_entity
        :param kwargs: 'db_entity_keys' Optional list to limit the Results processed. Any result whose
            result_db_entity_key or source_db_entity_key is in db_entity_keys will pass through.
        :return:
    """

    # Just process Scenarios. Projects, etc will probably have Results in the future
    if not isinstance(config_entity, Scenario):
        return

    db_entity_keys = kwargs.get('db_entity_keys', None)

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

    #for key, result_library in result_library_lookup.items():
    #    result_library.results.all().delete()

    # Create each configured Result
    for result_config in filter(lambda result:
                                    not db_entity_keys or
                                    result.result_db_entity_key in db_entity_keys or
                                    result.source_db_entity_key in db_entity_keys,
                                client_result.results()):

        logger.debug("\t\t\tResult Publishing Result DbEntity Key: %s" % result_config.result_db_entity_key)
        # Create the db_entity and db_entity_interest for the result
        db_entity = result_config.update_or_create_db_entity(config_entity)
        # Make the db_entity the default selected one for its key
        config_entity.select_db_entity_of_key(db_entity.key, db_entity)
        config_entity._no_post_save_publishing = True
        config_entity.save()
        config_entity._no_post_save_publishing = False


        # Test the query
        db_entity.parse_query(config_entity)

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


def on_config_entity_pre_delete_result(sender, **kwargs):
    """
    """
    config_entity = kwargs['instance']


