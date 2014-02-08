from django.db import models
from footprint.initialization.fixture import ProjectFixture
from footprint.initialization.fixtures.client.scag__irvine.base.scag_general_plan_parcel_feature import ScagGeneralPlanFeature
from footprint.initialization.fixtures.client.scag__irvine.base.scag_primary_spz_feature import ScagPrimarySPZFeature
from footprint.initialization.fixtures.client.scag__irvine.base.scag_jurisdiction_boundary_feature import ScagJurisdictionBoundaryFeature
from footprint.initialization.fixtures.client.scag__irvine.base.scag_sphere_of_influence_feature import ScagSphereOfInfluenceFeature
from footprint.initialization.fixtures.client.scag__irvine.base.scag_floodplain_feature import ScagFloodplainFeature
from footprint.initialization.fixtures.client.scag__irvine.base.scag_tier1_taz_feature import ScagTier1TazFeature
from footprint.initialization.fixtures.client.scag__irvine.base.scag_tier2_taz_feature import ScagTier2TazFeature
from footprint.initialization.fixtures.client.scag__irvine.base.scag_transit_areas_feature import ScagTransitAreasFeature
from footprint.initialization.fixtures.client.scag__irvine.base.scag_parks_open_space_feature import ScagParksOpenSpaceFeature
from footprint.initialization.fixtures.client.scag__irvine.base.scag_existing_land_use_parcel_feature import ScagExistingLandUseParcelFeature
from footprint.lib.functions import merge
from footprint.models import ConfigEntity
from footprint.models.keys.keys import Keys

__author__ = 'calthorpe'


class ScagIrvineProjectFixture(ProjectFixture):
    def feature_class_lookup(self):
        """
            Adds mappings of custom Feature classes
        :return:
        """
        parent_fixture = self.parent_fixture
        feature_class_lookup = parent_fixture.feature_class_lookup()
        return merge(feature_class_lookup, {
            Keys.DB_ABSTRACT_SCAG_EXISTING_LAND_USE_PARCEL_SOURCE: ScagExistingLandUseParcelFeature,
            Keys.DB_ABSTRACT_GENERAL_PLAN_FEATURE: ScagGeneralPlanFeature,
            Keys.DB_ABSTRACT_PRIMARY_SPZ_SOURCE: ScagPrimarySPZFeature,
            Keys.DB_ABSTRACT_JURISDICTION_BOUNDARY: ScagJurisdictionBoundaryFeature,
            Keys.DB_ABSTRACT_SPHERE_OF_INFLUENCE: ScagSphereOfInfluenceFeature,
            Keys.DB_ABSTRACT_FLOODPLAIN: ScagFloodplainFeature,
            Keys.DB_ABSTRACT_TIER1_TAZ: ScagTier1TazFeature,
            Keys.DB_ABSTRACT_TIER2_TAZ: ScagTier2TazFeature,
            Keys.DB_ABSTRACT_TRANSIT_AREAS: ScagTransitAreasFeature,
            Keys.DB_ABSTRACT_PARKS_OPEN_SPACE: ScagParksOpenSpaceFeature
        })

    def default_db_entity_setups(self):
        """
            Project specific SCAG additional db_entities
        :param default_dict:
        :return:
        """

        parent_fixture = self.parent_fixture
        defaults = parent_fixture.default_db_entity_setups()

        # SCAG PrimaryParcelFeature mapping updates
        def scag_existing_land_use_mapping(mapping):
            mapping['land_use_definition'] = {'land_use': 'land_use'}
            mapping['census_block'] = {'block': 'census_block'}
            mapping.pop('source_id')
            mapping.pop('uf_geometry_id')

        def scag_general_plan_land_use_mapping(mapping):
            mapping['land_use_definition'] = {'land_use': 'scag_general_plan_code'}
            mapping.pop('source_id')
            mapping.pop('uf_geometry_id')

        def source_id_mapping(mapping):
            mapping.pop('source_id')
            mapping.pop('uf_geometry_id')

        census_block_subclass = ConfigEntity.get_db_entity_setup(defaults, Keys.DB_ABSTRACT_CENSUS_BLOCK)[
            'feature_class']

        return super(ScagIrvineProjectFixture, self).default_db_entity_setups() + [
            self.config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_SCAG_EXISTING_LAND_USE_PARCEL_SOURCE,
                base_class=ScagExistingLandUseParcelFeature,
                fields=dict(
                    census_block=models.ForeignKey(census_block_subclass)
                ),
                import_table=True,
                source_id_column='source_id',
                import_mapping=scag_existing_land_use_mapping
            ),
            self.config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_GENERAL_PLAN_FEATURE,
                base_class=ScagGeneralPlanFeature,
                import_table=True,
                source_id_column='source_id',
                import_mapping=scag_general_plan_land_use_mapping
            ),

            self.config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_PRIMARY_SPZ_SOURCE,
                base_class=ScagPrimarySPZFeature,
                import_table=True,
                source_id_column='source_id',
                import_mapping=source_id_mapping
            ),
            self.config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_JURISDICTION_BOUNDARY,
                base_class=ScagJurisdictionBoundaryFeature,
                import_table=True,
                source_id_column='source_id',
                import_mapping=source_id_mapping
            ),

            self.config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_SPHERE_OF_INFLUENCE,
                base_class=ScagSphereOfInfluenceFeature,
                import_table=True,
                source_id_column='source_id',
                import_mapping=source_id_mapping
            ),

            self.config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_FLOODPLAIN,
                base_class=ScagFloodplainFeature,
                import_table=True,
                source_id_column='source_id',
                import_mapping=source_id_mapping
            ),

            self.config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_TIER1_TAZ,
                base_class=ScagTier1TazFeature,
                import_table=True,
                source_id_column='source_id',
                import_mapping=source_id_mapping
            ),
            self.config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_TIER2_TAZ,
                base_class=ScagTier2TazFeature,
                import_table=True,
                source_id_column='source_id',
                import_mapping=source_id_mapping
            ),

            self.config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_TRANSIT_AREAS,
                base_class=ScagTransitAreasFeature,
                import_table=True,
                source_id_column='source_id',
                import_mapping=source_id_mapping
            ),

            self.config_entity.create_db_entity_and_subclass(
                key=Keys.DB_ABSTRACT_PARKS_OPEN_SPACE,
                base_class=ScagParksOpenSpaceFeature,
                import_table=True,
                source_id_column='source_id',
                import_mapping=source_id_mapping
            )

        ]
