
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
from footprint.initialization.built_form.built_form_importer import BuiltFormImporter

from footprint.initialization.fixture import BuiltFormFixture, ConfigEntitiesFixture
from footprint.initialization.utils import resolve_fixture
from footprint.lib.functions import remove_keys, flatten
from footprint.models import GlobalConfig, Scenario
from footprint.models.built_form.built_form_set import BuiltFormSet
from footprint.models.built_form.flat_built_forms import refresh_all_flat_built_forms
import settings

built_form_fixture = resolve_fixture("built_form", "built_form", BuiltFormFixture, settings.CLIENT)

def built_form_sets():
    """
    Constructs and persists buildings, buildingtypes, and placetypes and their associates and then returns them all
    as a persisted BuiltFormSet. One BuiltFormSet is returned in an array
    :param test: if test is set to true, a much more limited set of built forms is created
    """

    # Create any built_form class sets that are configured for the client
    built_forms_dict = built_form_fixture.built_forms()
    built_form_fixture.tag_built_forms(built_forms_dict)
    built_forms = flatten(built_forms_dict.values())
    # Create/Refresh all the flat_built_forms in case anything changed
    refresh_all_flat_built_forms()

    return map(
        lambda built_form_set_config: update_or_create_built_form_set(built_form_set_config, built_forms),
        built_form_fixture.built_form_sets())


def update_or_create_built_form_set(built_form_set_config, built_forms):
    filtered_built_form_set_dict = remove_keys(built_form_set_config, ['clazz', 'keys', 'client'])
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
            built_form not in existing_built_forms and getattr(built_form, 'name', None) in client_built_form_names
        built_forms_for_set = filter(client_filter, built_forms_for_set)

    built_form_set.built_forms.add(*built_forms_for_set)
    return built_form_set


def on_config_entity_post_save_built_form(sender, **kwargs):
    """
        Sync a ConfigEntity's BuiltFormSets
    """
    config_entity = kwargs['instance']

    if isinstance(config_entity, GlobalConfig):
        # For now only the GlobalConfig creates the sets
        config_entity.add_built_form_sets(*(set(built_form_sets()) - set(config_entity.computed_built_form_sets())))
    elif isinstance(config_entity, Scenario) and kwargs['created']:
        # Scenarios set their selected built_form_set
        # This is a bit of hack to lookup the default built_form selection
        config_entities_fixture = resolve_fixture("config_entity", "config_entities", ConfigEntitiesFixture, config_entity.schema())
        scenario_fixture = filter(
            lambda scenario_fixture: scenario_fixture['key'] == config_entity.key,
            config_entities_fixture.scenarios())[0]
        built_form_set_selection_key = scenario_fixture.get('selections', {}).get('built_form_sets', None) if scenario_fixture else None
        try:
            config_entity.select_built_form_set(
                config_entity.computed_built_form_sets(key=built_form_set_selection_key)[0] if
                built_form_set_selection_key else
                config_entity.computed_built_form_sets()[0]
            )
        except Exception:
            raise Exception(
                "Bad built_form_set configuration for config_entity: {0}. Selected BuiltFormSet key: {1}, All BuiltFormSets".format(
                    config_entity, built_form_set_selection_key, config_entity.computed_built_form_sets()
                ))

def on_config_entity_pre_delete_built_form(sender, **kwargs):
    pass
