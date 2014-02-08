from django.db import models
from footprint.initialization.fixture import ProjectFixture
from footprint.initialization.fixtures.client.demo.base.demo_cpad_holdings_feature import DemoCpadHoldingsFeature
from footprint.initialization.fixtures.client.demo.base.demo_primary_parcel_feature import DemoPrimaryParcelFeature
from footprint.initialization.fixtures.client.demo.base.demo_stream_feature import DemoStreamFeature
from footprint.initialization.fixtures.client.demo.base.demo_vernal_pool_feature import DemoVernalPoolFeature
from footprint.initialization.fixtures.client.demo.base.demo_wetland_feature import DemoWetlandFeature
from footprint.initialization.utils import resolve_default_fixture
from footprint.lib.functions import merge
from footprint.models import ConfigEntity
from footprint.models.keys.keys import Keys

__author__ = 'calthorpe'


class DemoProjectFixture(ProjectFixture):
    def feature_class_lookup(self):
        """
            Adds mappings of custom Feature classes
        :return:
        """
        default_project = resolve_default_fixture("config_entity", "project", ProjectFixture, config_entity=None)
        feature_class_lookup = default_project.feature_class_lookup()
        return merge(feature_class_lookup, {
            Keys.DB_ABSTRACT_PRIMARY_PARCEL_SOURCE: DemoPrimaryParcelFeature,
            Keys.DB_ABSTRACT_VERNAL_POOL_FEATURE: DemoVernalPoolFeature,
            Keys.DB_ABSTRACT_WETLAND_FEATURE: DemoWetlandFeature,
            Keys.DB_ABSTRACT_STREAM_FEATURE: DemoStreamFeature,
            Keys.DB_ABSTRACT_CPAD_HOLDINGS_FEATURE: DemoCpadHoldingsFeature
        })

    def default_db_entity_setups(self):
        """
            Project specific SACOG additional db_entities
        :param default_dict:
        :return:
        """

        default_project_fixture = self.parent_fixture
        defaults = default_project_fixture.default_db_entity_setups()

        def primary_parcel_mapping(mapping):
            # Fill foreign key land_use_definition, using the matching values between
            #  LandUseDefinition.land_use and SacogPrimaryParcelFeature.landuse12
            mapping['land_use_definition'] = {'land_use': 'landuse12'}
            # Fill foreign key census_block, using the matching values between
            #  CensusBlock.block and the import field census_block
            mapping['census_block'] = {'block': 'census_block'}
            mapping.pop('source_id')
            mapping.pop('uf_geometry_id')

        census_block_subclass = ConfigEntity.get_db_entity_setup(defaults, Keys.DB_ABSTRACT_CENSUS_BLOCK)[
            'feature_class']

        def source_id_mapping(mapping):
            mapping.pop('source_id')
            mapping.pop('uf_geometry_id')

        return super(DemoProjectFixture, self).default_db_entity_setups() + [
            self.config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_PRIMARY_PARCEL_SOURCE,
                base_class=DemoPrimaryParcelFeature,
                fields=dict(
                    census_block=models.ForeignKey(census_block_subclass)
                ),
                import_table=True,
                source_id_column='source_id',
                import_mapping=primary_parcel_mapping
            ),
            self.config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_VERNAL_POOL_FEATURE,
                base_class=DemoVernalPoolFeature,
                import_table=True,
                source_id_column='source_id',
                import_mapping=source_id_mapping
            ),
            self.config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_WETLAND_FEATURE,
                base_class=DemoWetlandFeature,
                import_table=True,
                source_id_column='source_id',
                import_mapping=source_id_mapping
            ),
            self.config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_STREAM_FEATURE,
                base_class=DemoStreamFeature,
                import_table=True,
                source_id_column='source_id',
                import_mapping=source_id_mapping
            ),
            self.config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_CPAD_HOLDINGS_FEATURE,
                base_class=DemoCpadHoldingsFeature,
                import_table=True,
                source_id_column='source_id',
                import_mapping=source_id_mapping
            )
        ]