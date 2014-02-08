from footprint.initialization.fixture import GlobalConfigFixture
from footprint.initialization.fixtures.client.default.default_mixin import DefaultMixin
from footprint.initialization.utils import resolve_fixture
from footprint.lib.functions import map_dict, merge

__author__ = 'calthorpe'


class DefaultGlobalConfigFixture(DefaultMixin, GlobalConfigFixture):

    def feature_class_lookup(self):
        return {}

    def default_remote_db_entity_setups(self):
        googles = dict(
            hybrid="https://mt{S}.google.com/vt/lyrs=y&x={X}&y={Y}&z={Z}",
            satellite="https://khm{S}.google.com/kh/v=101&x={X}&y={Y}&z={Z}",
            labels="https://mts{S}.google.com/vt/lyrs=h@218000000&hl=en&src=app&x={X}&y={Y}&z={Z}",
            transit="https://mts{S}.google.com/vt/lyrs=m@219202286,transit:comp%7Cvm:1&hl=en&src=app&opts=r&x={X}&y={Y}&z={Z}&s=G"
        )
        google_setups = map_dict(
            lambda key, url: dict(
                key='google_%s' % key,
                url=url,
                hosts=["1", "2", "3"]),
            googles)

        cloudmade_setups = [dict(
            key='cloudmade_default',
            url="http://{S}tile.cloudmade.com/9c5e79c1284c4bbb838bc6d860d84921/998/256/{Z}/{X}/{Y}.png",
            hosts=["a.", "b.", "c.", ""])]
        return google_setups + cloudmade_setups

    def default_db_entity_setups(self):
        config_entity = self.config_entity
        remote_setups = self.default_remote_db_entity_setups()
        return map(
            lambda remote_setup: config_entity.create_db_entity(**remote_setup),
            remote_setups)
