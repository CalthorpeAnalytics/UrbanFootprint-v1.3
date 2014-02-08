from footprint.initialization.fixture import RegionFixture

__author__ = 'calthorpe'


class SacogRegionFixture(RegionFixture):

    def default_remote_db_entity_setups(self):
        return [dict(
            key='sacog_background',
            url="http://services.sacog.org/arcgis/rest/services/Imagery_DigitalGlobe_2012WGS/MapServer/tile/{Z}/{Y}/{X}"
        )]

    def default_db_entity_setups(self):
        """
            Region specific SACOG db_entity_setups
        :param default_dict:
        :return:
        """

        config_entity = self.config_entity
        parent_region_fixture = self.parent_fixture
        default_db_entity_setups = parent_region_fixture.default_db_entity_setups()

        remote_db_entity_setups = map(
            lambda remote_setup: config_entity.create_db_entity(**remote_setup),
            self.default_remote_db_entity_setups())

        return default_db_entity_setups + remote_db_entity_setups

