from footprint.main.models.geospatial.db_entity_configuration import create_db_entity_configuration
from footprint.client.configuration.fixture import GlobalConfigFixture
from footprint.client.configuration.default.default_mixin import DefaultMixin
from footprint.main.lib.functions import map_dict

__author__ = 'calthorpe_associates'


class DefaultGlobalConfigFixture(DefaultMixin, GlobalConfigFixture):

    def feature_class_lookup(self):
        return {}

    def default_remote_db_entity_configurations(self):
        googles = dict(
            aerial="https://mt{S}.google.com/vt/lyrs=y&x={X}&y={Y}&z={Z}",
            labels="https://mts{S}.google.com/vt/lyrs=h@218000000&hl=en&src=app&x={X}&y={Y}&z={Z}",
            map="https://mts{S}.google.com/vt/lyrs=m@219202286,transit:comp%7Cvm:1&hl=en&src=app&opts=r&x={X}&y={Y}&z={Z}&s=G",
        )
        google_setups = map_dict(
            lambda key, url: dict(
                key='google_%s' % key,
                url=url,
                hosts=["1", "2", "3"],
                no_feature_class_configuration=True),
            googles)

        cloudmade_setups = [dict(
            key='cloudmade_default',
            name='Cloudmade - Open Street Maps',
            url="http://{S}tile.cloudmade.com/9c5e79c1284c4bbb838bc6d860d84921/998/256/{Z}/{X}/{Y}.png",
            hosts=["a.", "b.", "c.", ""],
            no_feature_class_configuration=True)]
        return google_setups + cloudmade_setups

    def default_db_entity_configurations(self):
        config_entity = self.config_entity
        remote_db_entity_configurations = self.default_remote_db_entity_configurations()
        return map(
            lambda remote_db_entity_configuration: create_db_entity_configuration(config_entity, **remote_db_entity_configuration),
            remote_db_entity_configurations)

    def import_db_entity_configurations(self, **kwargs):
        return []
