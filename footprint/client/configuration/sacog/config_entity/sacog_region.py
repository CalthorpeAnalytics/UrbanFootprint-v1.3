
from footprint.main.models.geospatial.db_entity_configuration import create_db_entity_configuration
from footprint.client.configuration.fixture import RegionFixture
from footprint.main.models.keys.keys import Keys

__author__ = 'calthorpe_associates'


class SacogRegionFixture(RegionFixture):

    def default_remote_db_entity_configurations(self):
        """
            Add the SACOG background. This function is called from default_db_entity_configurations so it doesn't
            need to call the parent_fixture's method
        """
        return [dict(
            key='sacog_background',
            url="http://services.sacog.org/arcgis/rest/services/Imagery_DigitalGlobe_2012WGS/MapServer/tile/{Z}/{Y}/{X}",
            no_feature_class_configuration=True
        )]

    def default_db_entity_configurations(self):
        """
            Region specific SACOG db_entity_setups
        :param default_dict:
        :return:
        """

        config_entity = self.config_entity
        parent_region_fixture = self.parent_fixture
        default_db_entity_configurations = parent_region_fixture.default_db_entity_configurations()

        remote_db_entity_setups = map(
            lambda remote_setup: create_db_entity_configuration(config_entity, **remote_setup),
            self.default_remote_db_entity_configurations())

        return default_db_entity_configurations + remote_db_entity_setups

