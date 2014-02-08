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
import logging
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import Signal
# from memory_profiler import profile
from footprint.main.models.config.global_config import GlobalConfig
from footprint.main.models.config.config_entity import ConfigEntity
from footprint.main.publishing.publishing import post_save_publishing
from footprint.main.models.config.scenario import FutureScenario, BaseScenario
from footprint.main.models.config.project import Project
from footprint.main.models.config.region import Region
from footprint.main.publishing import tilestache_publishing, policy_publishing
from footprint.main.publishing import result_publishing
from footprint.main.publishing import db_entity_publishing
from footprint.main.publishing import data_import_publishing
from footprint.main.publishing import analysis_module_publishing
from footprint.main.publishing import layer_publishing
from footprint.main.publishing import built_form_publishing
from footprint.main.utils.subclasses import receiver_subclasses
from footprint.main.utils.utils import resolvable_module_attr_path

logger = logging.getLogger(__name__)

# Signal for all initial publishers. They can run without dependencies
post_save_config_entity_initial = Signal(providing_args=[])
# Signal for all publishers after built_forms are processed
post_save_config_entity_built_forms = Signal(providing_args=[])
# Signal for all publishers that can run after db_entities are processed
post_save_config_entity_db_entities = Signal(providing_args=[])
# Signal for all publishers that can run after layers are processed
post_save_config_entity_layers = Signal(providing_args=[])
# Signal for all publishers that can run after data importing
post_save_config_entity_imports = Signal(providing_args=[])
# Signal for all publishers that should run after analytic modules run
post_save_config_entity_analytic_run = Signal(providing_args=[])

def post_save_config_entity_initial_publishers(cls):
    """
        DbEntity publishing, Analysis Module publishing, and BuiltForm publishing can happen in parallel as soon
        as a config_entity is saved
    """
    post_save_config_entity_initial.connect(analysis_module_publishing.on_config_entity_post_save_analysis_modules, cls, True, "analysis_module_on_config_entity_post_save")

    post_save_config_entity_initial.connect(built_form_publishing.on_config_entity_post_save_built_form, cls, True, "built_form_publishing_on_config_entity_post_save")

    post_save_config_entity_initial.connect(policy_publishing.on_config_entity_post_save_policy, cls, True, "policy_publishing_on_config_entity_post_save")

def post_save_config_entity_built_form_publishers(cls):
    """
        DBEntity publishing can happen after built_forms
    """
    post_save_config_entity_built_forms.connect(db_entity_publishing.on_config_entity_post_save_db_entity, cls, True, "db_entity_on_config_entity_post_save")

def post_save_config_entity_db_entities_publishers(cls):
    """
        Data Import publishing, Layer publishing, and Result publishing can happen after DbEntity publishing
    """
    post_save_config_entity_db_entities.connect(data_import_publishing.on_config_entity_post_save_data_import, cls, True, "data_import_on_config_entity_post_save")

    post_save_config_entity_db_entities.connect(layer_publishing.on_config_entity_post_save_layer, cls, True, "layer_on_config_entity_post_save")

def post_save_config_entity_import_publishers(cls):
    """
        Result publishing can run after Data Import publishing
    """
    post_save_config_entity_imports.connect(result_publishing.on_config_entity_post_save_result, cls, True, "result_on_config_entity_post_save")

def post_save_config_entity_layers_publishers(cls):
    """
        Tilestache publishing can run after the Layer publisher
    """
    post_save_config_entity_layers.connect(tilestache_publishing.on_config_entity_post_save_tilestache, cls, True, "tilestache_on_config_entity_post_save")

def post_save_config_entity_analytic_runs_publishers(cls):
    """
        Tilestache also runs after analytic runs to clear the cache
        TODO this should be refined.
    """
    post_save_config_entity_analytic_run.connect(tilestache_publishing.on_post_analytic_run_tilestache, cls, True, "tilestache_on_post_analytic_run")

# Register receivers for only the lineage classes of Scenario subclasses
for cls in [FutureScenario, BaseScenario, Project, Region, GlobalConfig]:
    post_save_config_entity_initial_publishers(cls)
    post_save_config_entity_built_form_publishers(cls)
    post_save_config_entity_db_entities_publishers(cls)
    post_save_config_entity_import_publishers(cls)
    post_save_config_entity_layers_publishers(cls)
    post_save_config_entity_analytic_runs_publishers(cls)

def dependent_signal_paths(signal_path):
    """
        Gives the hierarchy of publisher signal calling order based on the given signal
        Signals are given as strings instead of paths for serialization ease
        param: signal_path. The signal path for which the dependent signals are returned
        return: An array of signal_paths or an empty array
    """

    if signal_path == resolvable_module_attr_path(__name__, 'post_save_config_entity_initial'):
        # BuiltForm dependent publishers can run after initial
        return [resolvable_module_attr_path(__name__, 'post_save_config_entity_built_forms')]
    elif signal_path == resolvable_module_attr_path(__name__, 'post_save_config_entity_built_forms'):
        # DbEntity dependent publishers can run after the built_form publishers
        return [resolvable_module_attr_path(__name__, 'post_save_config_entity_db_entities')]
    elif signal_path == resolvable_module_attr_path(__name__, 'post_save_config_entity_db_entities'):
        # Layer and DataImport dependent publishers are run after DbEntity dependent publishers
        return [resolvable_module_attr_path(__name__, 'post_save_config_entity_layers'),
                resolvable_module_attr_path(__name__, 'post_save_config_entity_imports')]
    return []

# Very wild guess about config_entity saving proportional times to send to the client
# These represent the parsed signal names sent to the client after the dependencies of
# the signal finish running
signal_proportion_lookup = dict(
    # Initial signals complete
    post_save_config_entity_initial=.20,
    # built_form dependants run after initial
    post_save_config_entity_built_forms=.20,
    # These run after built_forms
    post_save_config_entity_db_entities=.20,
    # layers and dataImports run in parallel after dbEntities
    post_save_config_entity_layers=.20,
    post_save_config_entity_imports=.20
)

@receiver_subclasses(pre_save, ConfigEntity, "config_entity_pre_save")
def on_config_entity_pre_save(sender, **kwargs):
    """
        A presave event handler. Currently this just defaults the bounds of the instance to those of its parent
    :param sender:
    :param kwargs:
    :return:
    """
    instance = kwargs['instance']
    if not instance.pk:
        # Inherit the parent's bounds if none are defined
        if not instance.bounds:
            instance.bounds = instance.parent_config_entity.bounds

@receiver_subclasses(post_save, ConfigEntity, "config_entity_post_save")
#@profile
def on_config_entity_post_save(sender, **kwargs):
    """
        Create the ConfigEntity's database schema on initial save.
        Post save starts a chain of asynchronous publishers that run according to a dependency tree.
        First publishers that are wired to the post_save_config_entity_initial signal
        run, followed by publishers dependent on signals that are dependent of
        post_save_config_entity_initial (see dependent_signal_paths)
        :param sender:
        :param kwargs:
        :return:
    """
    config_entity = kwargs['instance']

    for child_config_entity in config_entity.children():
        # Do any needed syncing of config_entity_children
        # This currently does nothing
        child_config_entity.parent_config_entity_saved()

    # Send a message to publishers to configure after creation or update of the config_entity
    # This is executed through a Celery task so that it can run asynchronously
    if config_entity._no_post_save_publishing:
        return
    if config_entity.deleted:
        # Also do nothing if the config_entity is deleted. At some point this should do some
        # processings, such as rekeying the scenario so it doesn't conflict with new scenario keys
        return

    if kwargs.get('created', None) and config_entity.origin_config_entity:
        config_entity.add_categories(*config_entity.origin_config_entity.categories.all())

    # TODO The default user here should be the admin, and in fact all config_entity instances
    # should simply have to have a creator
    user = config_entity.creator if config_entity.creator else User.objects.all()[0]
    starting_signal_path = resolvable_module_attr_path(__name__, 'post_save_config_entity_initial')

    logger.debug("Handler: post_save_config_entity for config_entity {config_entity} and user {username}".format(
        config_entity=config_entity,
        username=user.username))

    return post_save_publishing(
        starting_signal_path,
        config_entity,
        user,
        instance=config_entity,
        signal_proportion_lookup=signal_proportion_lookup,
        dependent_signal_paths=dependent_signal_paths,
        signal_prefix='post_save_config_entity')
