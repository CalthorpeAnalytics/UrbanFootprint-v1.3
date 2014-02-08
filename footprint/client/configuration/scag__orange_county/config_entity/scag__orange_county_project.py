from footprint.main.models.geospatial.db_entity_configuration import create_db_entity_configuration
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.client.configuration.fixture import ProjectFixture
from footprint.client.configuration.scag.base.scag_transit_areas_feature import ScagTransitAreasFeature
from footprint.main.lib.functions import merge
from footprint.main.models.base.base_parcel_feature import BaseParcelFeature
from footprint.main.models.keys.keys import Keys

__author__ = 'calthorpe_associates'


class ScagOrangeCountyProjectFixture(ProjectFixture):
    def feature_class_lookup(self):
        """
            Adds mappings of custom Feature classes
        :return:
        """
        parent_fixture = self.parent_fixture
        feature_class_lookup = parent_fixture.feature_class_lookup()
        return merge(
            feature_class_lookup,
            FeatureClassCreator.db_entity_key_to_feature_class_lookup(self.config_entity, self.default_db_entity_configurations())
        )

    def default_db_entity_configurations(self):
        """
            Project specific SCAG additional db_entities
        :return:
        """

        config_entity = self.config_entity

        return super(ScagOrangeCountyProjectFixture, self).default_db_entity_configurations(
            overrides={
                Keys.DB_ABSTRACT_BASE_FEATURE: dict(
                    # Override the name of the BaseFeature DbEntity to distinguish it from the parcel version below
                    name='Base SPZ Feature',
                    # Override the parcel class
                    geography_class_name='footprint.client.configuration.scag.models.geographies.spz.Spz'
                )
            }
        ) + [
            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_BASE_PARCEL_FEATURE,
                base_class=BaseParcelFeature,
                intersection=dict(type='centroid', to='polygon'),
                geography_class_name='footprint.main.models.geographies.parcel.Parcel',
                related_fields=dict(
                    built_form=dict(
                        single=True,
                        related_class_name='footprint.main.models.built_form.built_form.BuiltForm',
                        related_class_join_field_name='key',
                        source_class_join_field_name='built_form'))
            ),

            create_db_entity_configuration(config_entity,
                key=Keys.DB_ABSTRACT_TRANSIT_AREAS,
                base_class=ScagTransitAreasFeature,
                intersection=dict(type='polygon', to='centroid')
            )
        ]
