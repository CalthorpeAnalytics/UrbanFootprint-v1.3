from footprint.main.models.base.base_demographic_feature import BaseDemographicFeature
from footprint.main.models.geospatial.db_entity_configuration import create_db_entity_configuration
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.client.configuration.fixture import ProjectFixture, RegionFixture
from footprint.client.configuration.default.default_mixin import DefaultMixin
from footprint.client.configuration.utils import resolve_fixture
from footprint.main.lib.functions import merge
from footprint.main.models import CensusBlockgroup, CensusBlock, BaseFeature, DevelopableFeature
from footprint.main.models.analysis.vmt_features.vmt_trip_lengths_feature import VmtTripLengthsFeature
from footprint.main.models.base.census_tract import CensusTract
from footprint.main.models.base.cpad_holdings_feature import CpadHoldingsFeature
from footprint.main.models.keys.keys import Keys
from footprint.main.utils.utils import get_property_path

__author__ = 'calthorpe_associates'


class DefaultProjectFixture(DefaultMixin, ProjectFixture):

    def feature_class_lookup(self):
        # Get the client region fixture (or the default region if the former doesn't exist)
        client_region = resolve_fixture("config_entity", "region", RegionFixture)
        region_class_lookup = client_region.feature_class_lookup()
        return merge(
            region_class_lookup,
            FeatureClassCreator.db_entity_key_to_feature_class_lookup(self.config_entity, self.default_db_entity_configurations())
        )

    def default_db_entity_configurations(self, **kwargs):
        """
            Projects define DbEntities specific to the project, namely the Base table. To retrieve the subclass of a
            certain table, if it defines a base class here, use self.get_db_entity_class(Keys.KEY).
            kwargs: overrides can be supplied to override certain values. The override behavior must be hand-crafted
            below
        :return: a dictionary of
        """
        config_entity = self.config_entity

        return [
            create_db_entity_configuration(config_entity,
               key=Keys.DB_ABSTRACT_BASE_FEATURE,
               # If a name override is supplied, put it in. Otherwise leave null to derive it from the key
               name=get_property_path(kwargs, 'overrides.%s.name' % Keys.DB_ABSTRACT_BASE_FEATURE),
               # The Base Feature is normally considered a primary_geography unless overridden
               primary_geography=get_property_path(kwargs, 'overrides.%s.primary_geography' % Keys.DB_ABSTRACT_BASE_FEATURE) or True,
               primary_key='geography_id',
               primary_key_type='varchar',

               # The Base Feature is normally associated to a subclass of Geography unless overridden
               geography_class_name=get_property_path(kwargs, 'overrides.%s.geography_class_name' % Keys.DB_ABSTRACT_BASE_FEATURE) or
                                    'footprint.main.models.geographies.parcel.Parcel',
               extent_authority=True,
               base_class=BaseFeature,
               related_fields=dict(built_form=dict(
                   single=True,
                   related_class_name='footprint.main.models.built_form.built_form.BuiltForm',
                   related_class_join_field_name='key',
                   source_class_join_field_name='built_form_key'))
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_CENSUS_TRACT,
                base_class=CensusTract,
                intersection=dict(type='polygon', to='centroid')
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_CENSUS_BLOCKGROUP,
                base_class=CensusBlockgroup,
                intersection=dict(type='polygon', to='centroid'),
                related_fields=dict(census_tract=dict(
                    single=True,
                    related_db_entity_key=Keys.DB_ABSTRACT_CENSUS_TRACT,
                    related_class_join_field_name='tract',
                    source_class_join_field_name='tract'))
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_CENSUS_BLOCK,
                base_class=CensusBlock,
                intersection=dict(type='polygon', to='centroid'),
                fields=CensusBlock.dynamic_fields(),
                related_fields=dict(census_blockgroup=dict(
                    single=True,
                    related_db_entity_key=Keys.DB_ABSTRACT_CENSUS_BLOCKGROUP,
                    related_class_join_field_name='blockgroup',
                    source_class_join_field_name='blockgroup'))
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_DEVELOPABLE,
                base_class=DevelopableFeature,
                intersection=dict(type='attribute', db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE),
                primary_key='geography_id',
                primary_key_type='varchar'
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_CPAD_HOLDINGS_FEATURE,
                name='CPAD Holdings',
                base_class=CpadHoldingsFeature,
                intersection=dict(type='polygon')
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_BASE_DEMOGRAPHIC_FEATURE,
                base_class=BaseDemographicFeature,
                intersection=dict(type='attribute',  db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE),
                primary_key='geography_id',
                primary_key_type='varchar'
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_VMT_FUTURE_TRIP_LENGTHS_FEATURE,
                base_class=VmtTripLengthsFeature,
                intersection=dict(type='polygon', to='centroid')
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_VMT_BASE_TRIP_LENGTHS_FEATURE,
                base_class=VmtTripLengthsFeature,
                intersection=dict(type='polygon', to='centroid')
            )
        ]

    def import_db_entity_configurations(self, **kwargs):
        return []
