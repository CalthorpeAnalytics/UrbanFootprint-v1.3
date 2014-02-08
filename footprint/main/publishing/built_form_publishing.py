
# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
#from memory_profiler import profile
import os
from django.core.management import call_command
from footprint.main.initialization.built_form.built_form_importer import BuiltFormImporter
import logging
from footprint.client.configuration.fixture import BuiltFormFixture, ConfigEntitiesFixture
from footprint.client.configuration.utils import resolve_fixture
from footprint.main.lib.functions import remove_keys, flatten
from footprint.main.models import BuiltForm
from footprint.main.models.config.global_config import GlobalConfig
from footprint.main.models.config.scenario import Scenario
from footprint.main.models.config.region import Region
from footprint.main.models.built_form.built_form_set import BuiltFormSet
from footprint.main.models.built_form.flat_built_forms import refresh_all_flat_built_forms
from footprint import settings

logger = logging.getLogger(__name__)


#@profile
def on_config_entity_post_save_built_form(sender, **kwargs):
    """
        Sync a ConfigEntity's BuiltFormSets
    """
    config_entity = kwargs['instance']
    logger.debug("\t\tHandler: on_config_entity_post_save_built_form. ConfigEntity: %s" % config_entity.name)

    if isinstance(config_entity, GlobalConfig) or isinstance(config_entity, Region):
        # For now only the GlobalConfig and Regions creates the sets
        config_entity.add_built_form_sets(*(set(built_form_sets(config_entity)) - set(config_entity.computed_built_form_sets())))

    elif isinstance(config_entity, Scenario) and kwargs.get('created', None):
        # Scenarios set their selected built_form_set
        # This is a bit of hack to lookup the default built_form selection
        # TODO This needs to be replaced by a property on the config_entity, such as default_selections, copied from the ConfigEntityFixture
        # Looking up the fixture doesn't work for cloned ConfigEntities
        config_entities_fixture = resolve_fixture("config_entity", "config_entities", ConfigEntitiesFixture, config_entity.schema())
        scenario_fixtures = filter(
            lambda scenario_fixture: scenario_fixture['key'] == config_entity.key,
            config_entities_fixture.scenarios(config_entity.parent_config_entity))
        built_form_set_selection_key = scenario_fixtures[0].get('selections', {}).get('built_form_sets', None) \
            if len(scenario_fixtures) > 0 else None
        try:
            config_entity.select_built_form_set(
                config_entity.computed_built_form_sets(key=built_form_set_selection_key)[0] if
                built_form_set_selection_key else
                config_entity.computed_built_form_sets()[0]
            )
            config_entity._no_post_save_publishing = True
            config_entity.save()
            config_entity._no_post_save_publishing = False

        except Exception:
            raise Exception(
                "Bad built_form_set configuration for config_entity: {0}. Selected BuiltFormSet key: {1}, All BuiltFormSets".format(
                    config_entity, built_form_set_selection_key, config_entity.computed_built_form_sets()
                ))


def built_form_sets(config_entity):
    """
    Constructs and persists buildings, buildingtypes, and placetypes and their associates and then returns them all
    as a persisted BuiltFormSet. One BuiltFormSet is returned in an array
    :param test: if test is set to true, a much more limited set of built forms is created
    """
    json_fixture = os.path.join(settings.PROJECT_ROOT, 'built_form_fixture.json')
    built_form_fixture = resolve_fixture("built_form", "built_form", BuiltFormFixture, settings.CLIENT, config_entity=config_entity)

    if settings.IMPORT_BUILT_FORMS == 'CSV' or (not os.path.exists(json_fixture)):
        logger.info('Importing built forms from csv source')
        # Get the fixture scoped for the config_entity
        # Create any built_form class sets that are configured for the client at the config_entity's class scope
        built_forms_dict = built_form_fixture.built_forms()
        built_form_fixture.tag_built_forms(built_forms_dict)
        built_forms = flatten(built_forms_dict.values())
        if len(built_forms) > 0:
            # Create/Refresh all the flat_built_forms in case anything changed
            fixture_file = open(json_fixture, 'w')
            refresh_all_flat_built_forms()
            logger.debug('recreating fixture at ' + json_fixture)
            call_command('dumpdata', 'main.PrimaryComponentPercent', 'main.PlacetypeComponentPercent',
                         'main.BuildingUsePercent', 'main.BuiltFormSet', 'main.FlatBuiltForm', indent=2, stdout=fixture_file)
        else:
            logger.debug("skipping fixture / flat built form generation: nothing changed")
        return map(
            lambda built_form_set_config: update_or_create_built_form_set(built_form_set_config, built_forms),
            built_form_fixture.built_form_sets())

    elif settings.IMPORT_BUILT_FORMS == 'JSON' and not BuiltForm.objects.count():
        logger.info('Importing built forms from json fixture at ' + json_fixture)
        call_command('loaddata', json_fixture)
        return {}


def update_or_create_built_form_set(built_form_set_config, built_forms):
    filtered_built_form_set_dict = remove_keys(built_form_set_config, ['clazz', 'keys', 'client', 'scope'])
    built_form_set, created, updated = BuiltFormSet.objects.update_or_create(
        **dict(
            key=built_form_set_config['key'],
            defaults=dict(
                **filtered_built_form_set_dict
            )
        )
    )
    if not created:
        for key, value in filtered_built_form_set_dict.items():
            setattr(built_form_set, key, value)
        built_form_set.save()

    existing_built_forms = built_form_set.built_forms.all()

    # for the built_form_sets based on
    class_filter = lambda built_form: \
        built_form not in existing_built_forms and isinstance(built_form, built_form_set_config['clazz'])

    importer = BuiltFormImporter()

    built_forms_for_set = built_forms

    if built_form_set_config['clazz']:
        built_forms_for_set = filter(class_filter, built_forms_for_set)

    if built_form_set_config['client']:
        client = built_form_set_config['client']
        client_built_form_names = [bf.name for bf in importer.load_buildings_csv(client)] + \
            [bf.name for bf in importer.load_buildingtype_csv(client)] + \
            [bf.name for bf in importer.load_placetype_csv(client)]

        client_filter = lambda built_form: \
            built_form not in existing_built_forms and \
            (not client_built_form_names or getattr(built_form, 'name', None) in client_built_form_names)
        built_forms_for_set = filter(client_filter, built_forms_for_set)

    built_form_set.built_forms.add(*built_forms_for_set)
    return built_form_set


def on_config_entity_pre_delete_built_form(sender, **kwargs):
    pass
