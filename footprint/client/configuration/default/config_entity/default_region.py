from footprint.client.configuration.fixture import RegionFixture, GlobalConfigFixture
from footprint.client.configuration.default.default_mixin import DefaultMixin
from footprint.client.configuration.utils import resolve_fixture
from footprint.main.lib.functions import merge

__author__ = 'calthorpe_associates'


class DefaultRegionFixture(DefaultMixin, RegionFixture):

    def feature_class_lookup(self):
        # Get the client global_config fixture (or the default region if the former doesn't exist)
        client_global_config = resolve_fixture("config_entity", "global_config", GlobalConfigFixture)
        global_config_feature_class_lookup = client_global_config.feature_class_lookup()
        return merge(global_config_feature_class_lookup, {})

    def default_db_entities(self):
        """
            Region define DbEntities specific to the region.
            Currently there are none.
        """
        remote_db_entity_setups = self.default_remote_db_entity_configurations()
        return remote_db_entity_setups

    def import_db_entity_configurations(self, **kwargs):
        return []

    def default_behaviors(self, **kwargs):
        # Delegate to global. This allows clients to define Behaviors at the Region scope
        client_global_config = resolve_fixture("config_entity", "global_config", GlobalConfigFixture)
        return client_global_config.default_behaviors(**kwargs)
