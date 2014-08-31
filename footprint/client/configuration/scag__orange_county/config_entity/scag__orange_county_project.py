from footprint.client.configuration.scag.config_entity.scag_region import ScagDbEntityKey
from footprint.main.models import DbEntity
from footprint.main.models.geospatial.behavior import Behavior, BehaviorKey
from footprint.main.models.geospatial.db_entity_configuration import update_or_create_db_entity
from footprint.main.models.geospatial.feature import Feature
from footprint.main.models.geospatial.feature_behavior import FeatureBehavior
from footprint.main.models.geospatial.feature_class_configuration import FeatureClassConfiguration
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.client.configuration.fixture import ProjectFixture
from footprint.main.lib.functions import merge
from footprint.main.models.base.base_parcel_feature import BaseParcelFeature

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
            FeatureClassCreator.key_to_dynamic_model_class_lookup(self.config_entity, self.default_db_entities())
        )

    def default_db_entities(self):
        """
            Project specific SCAG additional db_entities
        :return:
        """

        project = self.config_entity
        # The DbEntity keyspace. These keys have no prefix
        Key = ScagDbEntityKey
        # The Behavior keyspace
        behavior_key = BehaviorKey.Fab.ricate
        # Used to load Behaviors defined elsewhere
        get_behavior = lambda key: Behavior.objects.get(key=behavior_key(key))

        return super(ScagOrangeCountyProjectFixture, self).default_db_entities(
            overrides={
                ScagDbEntityKey.BASE: dict(
                    # Override the name of the BaseFeature DbEntity to distinguish it from the parcel version below
                    name='Base SPZ Feature',
                    # Override the parcel class
                    geography_class_name='footprint.client.configuration.scag.models.geographies.spz.Spz'
                )
            }
        ) + [
            update_or_create_db_entity(project, DbEntity(
                key=Key.BASE_PARCEL,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=BaseParcelFeature,
                    geography_class_name='footprint.main.models.geographies.parcel.Parcel',
                    related_fields=dict(
                        built_form=dict(
                            single=True,
                            related_class_name='footprint.main.models.built_form.built_form.BuiltForm',
                            related_class_join_field_name='key',
                            source_class_join_field_name='built_form')
                    )
                ),
                feature_behavior=FeatureBehavior(
                    get_behavior('base')
                )
            )),

            update_or_create_db_entity(project, DbEntity(
                key=Key.TRANSIT_AREAS,
                feature_class_configuration=FeatureClassConfiguration(
                    abstract_class=Feature
                ),
                feature_behavior=FeatureBehavior(
                    get_behavior('transit')
                )
            ))
        ]
