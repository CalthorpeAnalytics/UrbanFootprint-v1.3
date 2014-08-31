
# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2014 Calthorpe Associates
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
from django.db.models.signals import post_save
from django.dispatch import Signal
from footprint.main.initialization.built_form.built_form_importer import BuiltFormImporter
import logging
from footprint.main.lib.functions import remove_keys, flatten
from footprint.main.models.built_form.built_form import BuiltForm
from footprint.main.models.built_form.placetype import Placetype
from footprint.main.models.built_form.placetype_component import PlacetypeComponent
from footprint.main.models.built_form.primary_component import PrimaryComponent
from footprint.main.models.built_form.agriculture.crop import Crop
from footprint.main.models.built_form.agriculture.crop_type import CropType
from footprint.main.models.built_form.urban.building import Building
from footprint.main.models.built_form.urban.building_type import BuildingType
from footprint.main.models.built_form.urban.urban_placetype import UrbanPlacetype
from footprint.main.models.built_form.agriculture.landscape_type import LandscapeType
from footprint.main.models.config.global_config import GlobalConfig
from footprint.main.models.config.scenario import Scenario
from footprint.main.models.config.region import Region
from footprint.main.models.built_form.built_form_set import BuiltFormSet
from footprint import settings
from footprint.main.publishing import tilestache_publishing, layer_publishing
from footprint.main.publishing.publishing import post_save_publishing
from footprint.main.utils.subclasses import receiver_subclasses
from footprint.main.utils.utils import resolvable_module_attr_path

logger = logging.getLogger(__name__)

# Signal for all initial publishers. They can run without dependencies
post_save_built_form_initial = Signal(providing_args=["agriculture"])
post_save_built_form_layer = Signal(providing_args=["agriculture"])


def post_save_built_form_publishers(cls):
    """
        DbEntity publishing, Analysis Module publishing, and BuiltForm publishing can happen in parallel as soon
        as a config_entity is saved
    """
    post_save_built_form_initial.connect(layer_publishing.on_post_save_built_form_layer, cls,
                                         True, "layer_publishing_on_built_form_post_save")
    post_save_built_form_layer.connect(tilestache_publishing.on_post_save_built_form_tilestache, cls,
                                       True, "tilestache_publishing_on_built_form_post_save")


for cls in [Placetype, PlacetypeComponent, PrimaryComponent, UrbanPlacetype, BuildingType, Building, LandscapeType, CropType, Crop]:
    post_save_built_form_publishers(cls)

signal_proportion_lookup = dict(
    post_save_built_form_initial=.5,
    post_save_built_form_layer=.5,
)


def dependent_signal_paths(signal_path):
    if signal_path == resolvable_module_attr_path(__name__, 'post_save_built_form_initial'):
        return [resolvable_module_attr_path(__name__, 'post_save_built_form_layer')]
    return []


@receiver_subclasses(post_save, BuiltForm, "built_form_post_save")
def on_built_form_post_save(sender, **kwargs):

    built_form = kwargs['instance']
    if kwargs.get('created', None) and built_form.origin_instance:
        # If a clone occurred copy the clone into the same BuiltFormSets
        for built_form_set in built_form.origin_instance.builtformset_set.filter(deleted=False):
            built_form_set.built_forms.add(built_form)

    if not built_form.no_post_save_publishing:
        built_form_save_aggregates_and_publishing(built_form)

def built_form_save_aggregates_and_publishing(built_form):
    """
        Post save starts a chain of asynchronous publishers that run according to a dependency tree.
        First publishers that are wired to the post_save_built_form_initial signal
        run, followed by publishers dependent on signals that are dependent on that signal
        :param built_form: The BuiltForm
    """

    # Send a message to publishers to configure after creation or update of the config_entity
    # This is executed through a Celery task so that it can run asynchronously
    if BuiltForm._no_post_save_publishing or built_form.no_post_save_publishing:
        return

    if built_form.deleted:
        # Also do nothing if the built_form is deleted. At some point this should do some
        # processings, such as rekeying the built_form so it doesn't conflict with new keys
        return

    # Update or create the flat built form
    built_form.on_instance_modify()

    return _on_built_form_post_save(built_form)


def _on_built_form_post_save(built_form):
    logger.debug("Handler: post_save_built_form for {built_form}".format(built_form=built_form))
    user = built_form.updater
    starting_signal_path = resolvable_module_attr_path(__name__, 'post_save_built_form_initial')
    return post_save_publishing(
        starting_signal_path,
        None,
        user,
        instance=built_form,
        signal_proportion_lookup=signal_proportion_lookup,
        dependent_signal_paths=dependent_signal_paths,
        signal_prefix='post_save_built_form')


def on_config_entity_post_save_built_form(sender, **kwargs):
    """
        Sync a ConfigEntity's BuiltFormSets
    """

    # Turn off BuiltForm instances own post-save publishing with this class scope flag
    # The ConfigEntity is managing creation and update, so we don't want to trigger publishers after every
    # BuiltForm is created/updated

    from footprint.client.configuration.fixture import ConfigEntitiesFixture
    from footprint.client.configuration.utils import resolve_fixture

    BuiltForm.no_post_save_publishing = True

    config_entity = kwargs['instance']
    logger.debug("\t\tHandler: on_config_entity_post_save_built_form. ConfigEntity: %s" % config_entity.name)

    if isinstance(config_entity, GlobalConfig) or isinstance(config_entity, Region):
        # For now only the GlobalConfig and Regions creates the sets
        config_entity.add_built_form_sets(*(set(built_form_sets(config_entity)) - set(config_entity.computed_built_form_sets())))

    elif isinstance(config_entity, Scenario):  # and kwargs.get('created', None):
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
            previous = config_entity._no_post_save_publishing
            config_entity._no_post_save_publishing = True
            config_entity.save()
            config_entity._no_post_save_publishing = previous

        except Exception:
            raise Exception(
                "Bad built_form_set configuration for config_entity: {0}. Selected BuiltFormSet key: {1}, All BuiltFormSets".format(
                    config_entity, built_form_set_selection_key, config_entity.computed_built_form_sets()
                ))
    BuiltForm.no_post_save_publishing = False


def built_form_sets(config_entity):
    """
    Constructs and persists buildings, buildingtypes, and placetypes and their associates and then returns them all
    as a persisted BuiltFormSet. One BuiltFormSet is returned in an array
    :param test: if test is set to true, a much more limited set of built forms is created
    """
    from footprint.client.configuration.fixture import BuiltFormFixture
    from footprint.client.configuration.utils import resolve_fixture

    json_fixture = os.path.join(settings.PROJECT_ROOT, 'built_form_fixture.json')
    built_form_fixture = resolve_fixture("built_form", "built_form", BuiltFormFixture, settings.CLIENT, config_entity=config_entity)

    if settings.IMPORT_BUILT_FORMS == 'CSV' or (not os.path.exists(json_fixture)):
        logger.info('Importing built forms from csv source')
        # Get the fixture scoped for the config_entity
        # Create any built_form class sets that are configured for the client at the config_entity's class scope
        built_forms_dict = built_form_fixture.built_forms()
        built_form_fixture.tag_built_forms(built_forms_dict)
        built_forms = flatten(built_forms_dict.values())

        return map(
            lambda built_form_set_config: update_or_create_built_form_set(built_form_set_config, built_forms),
            built_form_fixture.built_form_sets())

    elif settings.IMPORT_BUILT_FORMS == 'JSON' and not BuiltForm.objects.count():
        logger.info('Importing built forms from json fixture at ' + json_fixture)
        call_command('loaddata', json_fixture)
        return {}


def update_or_create_built_form_set(built_form_set_config, built_forms):
    filtered_built_form_set_dict = remove_keys(built_form_set_config, ['clazz', 'keys', 'client', 'scope', 'attribute'])
    built_form_set, created, updated = BuiltFormSet.objects.update_or_create(
        **dict(
            key=built_form_set_config['key'],
            defaults=dict(**filtered_built_form_set_dict)
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

    attribute_filter = lambda built_form: \
        built_form not in existing_built_forms and getattr(built_form, built_form_set_config['attribute'], None)

    importer = BuiltFormImporter()

    built_forms_for_set = built_forms

    if built_form_set_config['clazz']:
        built_forms_for_set = filter(class_filter, built_forms_for_set)

    if built_form_set_config['attribute']:
        built_forms_for_set = filter(attribute_filter, built_forms_for_set)

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
