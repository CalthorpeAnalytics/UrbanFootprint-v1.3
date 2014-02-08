from django.db import models
from footprint.main.models.geospatial.db_entity_configuration import create_db_entity_configuration, db_entity_key_to_feature_class_lookup
from footprint.client.configuration.fixture import ProjectFixture
from footprint.client.configuration.scag.base.scag_transit_areas_feature import ScagTransitAreasFeature
from footprint.client.configuration.scag__irvine.base.scag_general_plan_parcel_feature import ScagGeneralPlanParcelFeature
from footprint.client.configuration.scag__irvine.base.scag_primary_spz_feature import ScagPrimarySPZFeature
from footprint.client.configuration.scag__irvine.base.scag_jurisdiction_boundary_feature import ScagJurisdictionBoundaryFeature
from footprint.client.configuration.scag__irvine.base.scag_sphere_of_influence_feature import ScagSphereOfInfluenceFeature
from footprint.client.configuration.scag__irvine.base.scag_floodplain_feature import ScagFloodplainFeature
from footprint.client.configuration.scag__irvine.base.scag_tier1_taz_feature import ScagTier1TazFeature
from footprint.client.configuration.scag__irvine.base.scag_tier2_taz_feature import ScagTier2TazFeature
from footprint.client.configuration.scag__irvine.base.scag_parks_open_space_feature import ScagParksOpenSpaceFeature
from footprint.client.configuration.scag__irvine.base.scag_existing_land_use_parcel_feature import ScagExistingLandUseParcelFeature
from footprint.main.lib.functions import merge
from footprint.main.models import ConfigEntity
from footprint.main.models.keys.keys import Keys

__author__ = 'calthorpe_associates'


class ScagIrvineProjectFixture(ProjectFixture):

    def default_db_entity_configurations(self):
        """
            Project specific SCAG additional db_entities
        :param default_dict:
        :return:
        """

        parent_fixture = self.parent_fixture
        defaults = parent_fixture.default_db_entity_configurations()
        config_entity = self.config_entity

        return super(ScagIrvineProjectFixture, self).default_db_entity_configurations() + [
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_SCAG_EXISTING_LAND_USE_PARCEL_SOURCE,
                base_class=ScagExistingLandUseParcelFeature,
                primary_geography=True,
                related_fields=dict(
                    land_use_definition=dict(
                        single=True,
                        related_class_name='footprint.client.configuration.sacog.built_form.scag_land_use_definition.ScagLandUseDefinition',
                        related_class_join_field_name='land_use',
                        source_class_join_field_name='land_use'),
                    ),
                    census_blocks=dict(
                        single=True,
                        related_db_entity_key=Keys.DB_ABSTRACT_CENSUS_BLOCK,
                        related_class_join_field_name='block',
                        source_class_join_field_name='census_block',
                    )
            ),
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_GENERAL_PLAN_FEATURE,
                base_class=ScagGeneralPlanParcelFeature,
                intersection=dict(type='polygon', to='centroid'),
                related_fields=dict(
                    land_use_definition=dict(
                    single=True,
                    related_class_name='footprint.client.configuration.sacog.built_form.scag_land_use_definition.ScagLandUseDefinition',
                    related_class_join_field_name='land_use',
                    source_class_join_field_name='scag_general_plan_code'))
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_PRIMARY_SPZ_SOURCE,
                base_class=ScagPrimarySPZFeature,
                primary_geography=True
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_JURISDICTION_BOUNDARY,
                base_class=ScagJurisdictionBoundaryFeature,
                intersection=dict(type='polygon', to='centroid')
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_SPHERE_OF_INFLUENCE,
                base_class=ScagSphereOfInfluenceFeature,
                intersection=dict(type='polygon', to='centroid')
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_FLOODPLAIN,
                base_class=ScagFloodplainFeature,
                intersection=dict(type='polygon')
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_TIER1_TAZ,
                base_class=ScagTier1TazFeature,
                intersection=dict(type='polygon', to='centroid')
            ),
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_TIER2_TAZ,
                base_class=ScagTier2TazFeature,
                intersection=dict(type='polygon', to='centroid')
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_PARKS_OPEN_SPACE,
                base_class=ScagParksOpenSpaceFeature,
                intersection=dict(type='polygon')
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_TRANSIT_AREAS,
                base_class=ScagTransitAreasFeature,
                intersection=dict(type='polygon', to='centroid')
            )

        ]
