from footprint.initialization.fixture import ProjectFixture, RegionFixture
from footprint.initialization.fixtures.client.default.default_mixin import DefaultMixin
from footprint.initialization.utils import resolve_fixture
from footprint.lib.functions import merge
from footprint.models import CensusBlockgroup, CensusBlock, BaseFeature, DevelopableFeature
from footprint.models.base.base_parcel_feature import BaseParcelFeature
from footprint.models.base.census_tract import CensusTract
from footprint.models.base.cpad_holdings_feature import CpadHoldingsFeature
from footprint.models.keys.keys import Keys

__author__ = 'calthorpe'


class DefaultProjectFixture(DefaultMixin, ProjectFixture):
    def feature_class_lookup(self):
        # Get the client region fixture (or the default region if the former doesn't exist)
        client_region = resolve_fixture("config_entity", "region", RegionFixture)
        region_class_lookup = client_region.feature_class_lookup()
        return merge(region_class_lookup, {
            Keys.DB_ABSTRACT_CENSUS_TRACT: CensusTract,
            Keys.DB_ABSTRACT_CENSUS_BLOCKGROUP: CensusBlockgroup,
            Keys.DB_ABSTRACT_CENSUS_BLOCK: CensusBlock,
            Keys.DB_ABSTRACT_BASE_FEATURE: BaseFeature,
            Keys.DB_ABSTRACT_BASE_PARCEL_FEATURE: BaseParcelFeature,
            Keys.DB_ABSTRACT_DEVELOPABLE: DevelopableFeature,
            Keys.DB_ABSTRACT_CPAD_HOLDINGS_FEATURE: CpadHoldingsFeature
        })

    def default_db_entity_setups(self):
        """
            Projects define DbEntities specific to the project, namely the Base table. To retrieve the subclass of a
            certain table, if it defines a base class here, use self.get_db_entity_class(Keys.KEY).
        :return: a dictionary of
        """
        config_entity = self.config_entity


        def census_block_mapping(mapping):
            mapping['census_blockgroup'] = {'blockgroup': 'blockgroup'}
            mapping.pop('blockgroup')
            mapping.pop('uf_geometry_id')

        def census_blockgroup_mapping(mapping):
            mapping['census_tract'] = {'tract': 'tract'}
            mapping.pop('tract')
            mapping.pop('uf_geometry_id')

        def census_tract_mapping(mapping):
            mapping.pop('uf_geometry_id')

        def base_feature_mapping(mapping):
            mapping['built_form'] = {'key': 'built_form'}
            mapping.pop('geography_id')
            mapping.pop('uf_geometry_id')

        def base_parcel_feature_mapping(mapping):
            mapping['built_form'] = {'key': 'built_form'}
            mapping.pop('geography_id')
            mapping.pop('uf_geometry_id')

        def developable_feature_mapping(mapping):
            mapping.pop('geography_id')
            mapping.pop('uf_geometry_id')

        def cpad_holdings_feature_mapping(mapping):
            mapping.pop('source_id')
            mapping.pop('uf_geometry_id')

        census_tract_db_entity_and_subclass = config_entity.create_db_entity_and_subclass(
            key=Keys.DB_ABSTRACT_CENSUS_TRACT,
            base_class=CensusTract,
            source_id_column='tract',
            import_table=True,
            import_mapping=census_tract_mapping)

        census_blockgroup_db_entity_and_subclass = config_entity.create_db_entity_and_subclass(
            key=Keys.DB_ABSTRACT_CENSUS_BLOCKGROUP,
            base_class=CensusBlockgroup,
            extent_authority=True,
            fields=CensusBlockgroup.dynamic_fields(census_tract=census_tract_db_entity_and_subclass),
            source_id_column='blockgroup',
            import_table=True,
            import_mapping=census_blockgroup_mapping)

        census_block_db_entity_and_subclass = config_entity.create_db_entity_and_subclass(
            key=Keys.DB_ABSTRACT_CENSUS_BLOCK,
            base_class=CensusBlock,
            fields=CensusBlock.dynamic_fields(census_blockgroup=census_blockgroup_db_entity_and_subclass),
            source_id_column='block',
            import_table=True,
            import_mapping=census_block_mapping)

        developable_db_entity_and_subclass = config_entity.create_db_entity_and_subclass(
            key=Keys.DB_ABSTRACT_DEVELOPABLE,
            source_id_column='geography_id',
            base_class=DevelopableFeature,
            import_table=True,
            import_mapping=developable_feature_mapping)

        cpad_holdings_db_entity_and_subclass = config_entity.create_db_entity_and_subclass(
            key=Keys.DB_ABSTRACT_CPAD_HOLDINGS_FEATURE,
            source_id_column='source_id',
            base_class=CpadHoldingsFeature,
            import_table=True,
            import_mapping=cpad_holdings_feature_mapping)

        base_parcel_feature_db_entity_and_subclass = config_entity.create_db_entity_and_subclass(
            key=Keys.DB_ABSTRACT_BASE_PARCEL_FEATURE,
            source_id_column='geography_id',
            base_class=BaseParcelFeature,
            import_table=True,
            import_mapping=base_parcel_feature_mapping)

        return [
            census_tract_db_entity_and_subclass,
            census_blockgroup_db_entity_and_subclass,
            census_block_db_entity_and_subclass,
            developable_db_entity_and_subclass,
            cpad_holdings_db_entity_and_subclass,
            base_parcel_feature_db_entity_and_subclass,
            config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_BASE_FEATURE,
                base_class=BaseFeature,
                source_id_column='geography_id',
                import_table=True,
                import_mapping=base_feature_mapping
            )
        ]

