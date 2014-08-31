from django.contrib.auth.models import User
from footprint.main.models import DbEntity, FeatureBehavior
from footprint.main.models.geospatial.behavior import Behavior, BehaviorKey, update_or_create_behavior
from footprint.main.models.geospatial.db_entity_configuration import update_or_create_db_entity
from footprint.client.configuration.fixture import GlobalConfigFixture
from footprint.client.configuration.default.default_mixin import DefaultMixin
from footprint.main.lib.functions import map_dict
from footprint.main.models.geospatial.intersection import Intersection, IntersectionKey

__author__ = 'calthorpe_associates'


class DefaultGlobalConfigFixture(DefaultMixin, GlobalConfigFixture):

    def feature_class_lookup(self):
        return {}

    def default_remote_db_entity_configurations(self):
        # The Behavior keyspace
        behavior_key = BehaviorKey.Fab.ricate
        # Used to load Behaviors defined elsewhere
        get_behavior = lambda key: Behavior.objects.get(key=behavior_key(key))

        googles = dict(
            aerial="https://mt{S}.google.com/vt/lyrs=y&x={X}&y={Y}&z={Z}",
            labels="https://mts{S}.google.com/vt/lyrs=h@218000000&hl=en&src=app&x={X}&y={Y}&z={Z}",
            map="https://mts{S}.google.com/vt/lyrs=m@219202286,transit:comp%7Cvm:1&hl=en&src=app&opts=r&x={X}&y={Y}&z={Z}&s=G",
        )
        google_setups = map_dict(
            lambda key, url: DbEntity(
                key='google_%s' % key,
                url=url,
                hosts=["1", "2", "3"],
                no_feature_class_configuration=True,
                feature_behavior=FeatureBehavior(
                    behavior=get_behavior('remote_imagery')
                ),
            ),
            googles)

        cloudmade_setups = [DbEntity(
            key='cloudmade_default',
            name='Cloudmade - Open Street Maps',
            url="http://{S}tile.cloudmade.com/9c5e79c1284c4bbb838bc6d860d84921/998/256/{Z}/{X}/{Y}.png",
            hosts=["a.", "b.", "c.", ""],
            no_feature_class_configuration=True,
            feature_behavior=FeatureBehavior(
                behavior=get_behavior('remote_imagery')
            ),
        )]
        return google_setups + cloudmade_setups

    def default_db_entities(self):
        config_entity = self.config_entity
        remote_db_entity_configurations = self.default_remote_db_entity_configurations()
        return map(
            lambda remote_db_entity_configuration: update_or_create_db_entity(
                config_entity,
                remote_db_entity_configuration),
            remote_db_entity_configurations)

    def import_db_entity_configurations(self, **kwargs):
        return []

    def default_behaviors(self, **kwargs):
        key = BehaviorKey.Fab.ricate
        # This doesn't fetch from the database, since the Behavior being sought might not exist quite yet
        get_behavior = lambda raw_key: Behavior(key=key(raw_key))
        polygon = IntersectionKey.POLYGON
        centroid = IntersectionKey.CENTROID

        # Create a special DbEntity used only by Behavior.feature_template_behavior instances
        dummy_user = User.objects.all()[0]

        DbEntity.objects.update_or_create(key='template_feature_behavior', defaults=dict(creator=dummy_user, updater=dummy_user))

        return map(lambda behavior: update_or_create_behavior(behavior), [
            Behavior(
                key=key('constraint'),
                abstract=True
            ),
            Behavior(
                key=key('environmental'),
                abstract=True
            ),
            Behavior(
                key=key('environmental_constraint'),
                parents=[
                    get_behavior('constraint'),
                    get_behavior('environmental')
                ],
                # Environmental constraints always intersect primary features polygon to polygon
                intersection=Intersection(from_type=polygon, to_type=polygon)
            ),
            # A behavior attributed to Features representing UrbanFootprint base data
            Behavior(
                key=key('base')
            ),
            Behavior(
                key=key('base_feature'),
                parents=[get_behavior('base')],
                # I'm not sure why this would ever need an intersection, being a primary geography, but scag__orange had it
                intersection=Intersection(from_type=centroid, to_type=polygon),
                abstract=True
            ),
            Behavior(
                key=key('census'),
                parents=[
                    get_behavior('base')
                ],
                # Census features intersect polygon to centroid.
                intersection=Intersection(from_type=polygon, to_type=centroid),
            ),
            Behavior(
                key=key('developable'),
                parents=[],
                # Intersects using an attribute intersection with the table
                # specified in the DbEntity's feature_behavior.intersection['db_entity_key']
                intersection=Intersection(join_type=IntersectionKey.ATTRIBUTE),
                abstract=True
            ),
            Behavior(
                key=key('cpad'),
                parents=[
                    # TODO should constraint also be a parent??
                    get_behavior('base')
                ],
                intersection=Intersection(from_type=polygon, to_type=polygon),
                abstract=True
            ),
            # Describes demographic behavior. This is just used as a parent of base_demographic for now
            Behavior(
                key=key('demographic'),
                parents=[],
                abstract=True
            ),
            Behavior(
                key=key('travel'),
                parents=[]
            ),
            Behavior(
                key=key('trips'),
                parents=[get_behavior('travel')],
                abstract=True
            ),
            Behavior(
                key=key('climate'),
                parents=[get_behavior('climate')]
            ),
            Behavior(
                key=key('future'),
                parents=[]
            ),
            Behavior(
                key=key('future_output'),
                parents=[get_behavior('future')],
                abstract=True
            ),
            Behavior(
                key=key('agriculture'),
                parents=[],
                abstract=True
            ),
            Behavior(
                key=key('future_agriculture'),
                parents=[get_behavior('future'), get_behavior('agriculture')],
                abstract=True
            ),
            Behavior(
                key=key('future_developable'),
                parents=[get_behavior('future'), get_behavior('developable')],
                abstract=True
            ),
            Behavior(
                key=key('buffer'),
                parents=[],
                intersection=Intersection(from_type='polygon', to_type='polygon')
            ),
            Behavior(
                key=key('travel_buffer'),
                parents=[get_behavior('travel'), get_behavior('buffer')],
                intersection=Intersection(from_type='polygon', to_type='polygon')
            ),
            Behavior(
                key=key('energy'),
                parents=[]
            ),
            Behavior(
                key=key('water'),
                parents=[]
            ),
            Behavior(
                key=key('land_consumption'),
                parents=[],
                abstract=True
            ),
            Behavior(
                key=key('existing_land_use'),
                parents=[get_behavior('base')],
                abstract=True
            ),
            Behavior(
                key=key('transit'),
                parents=[get_behavior('travel')]
            ),
            Behavior(
                key=key('transit_line'),
                parents=[get_behavior('transit')],
            ),
            Behavior(
                key=key('transit_stop'),
                parents=[get_behavior('transit')],
                intersection=Intersection(from_type='centroid', to_type='polygon')
            ),
            Behavior(
                key=key('travel_network'),
                parents=[get_behavior('travel')],
                intersection=Intersection(from_type='polygon', to_type='polygon'),
                abstract=True
            ),
            Behavior(
                key=key('transit_network'),
                parents=[get_behavior('transit'), get_behavior('travel_network')],
                intersection=Intersection(from_type='polygon', to_type='polygon')
            ),
            Behavior(
                key=key('light_rail'),
                parents=[get_behavior('transit')],
                abstract=True
            ),
            Behavior(
                key=key('light_rail_line'),
                parents=[get_behavior('light_rail'), get_behavior('transit_line')],
                # TODO I'm not sure why light_rail uses a polygon intersection
                # This should be clarified or removed from here and put on specific FeatureBeahvior instances
                intersection=Intersection(from_type='polygon', to_type='polygon'),
                abstract=True
            ),
            Behavior(
                key=key('light_rail_stop'),
                parents=[get_behavior('light_rail'), get_behavior('transit_stop')],
                intersection=Intersection(from_type='polygon', to_type='polygon'),
                abstract=True
            ),
            Behavior(
                key=key('transit_buffer'),
                parents=[get_behavior('light_rail'), get_behavior('transit_stop'), get_behavior('travel_buffer')],
                intersection=Intersection(from_type='polygon', to_type='centroid')
            ),
            Behavior(
                key=key('boundary'),
                parents=[],
                intersection=Intersection(from_type='polygon', to_type='centroid'),
                abstract=True
            ),
            Behavior(
                key=key('general_plan'),
                parents=[],
                intersection=Intersection(from_type='polygon', to_type='centroid'),
                abstract=True
            ),
            Behavior(
                key=key('taz'),
                parents=[get_behavior('travel')],
                intersection=Intersection(from_type='polygon', to_type='centroid'),
                abstract=True
            ),
            Behavior(
                key=key('transit_area'),
                parents=[get_behavior('transit')],
                intersection=Intersection(from_type='polygon', to_type='centroid'),
                abstract=True
            ),
            Behavior(
                key=key('fiscal'),
                parents=[],
                abstract=True
            ),
            Behavior(
                key=key('census_tract'),
                parents=[get_behavior('census')],
                abstract=True
            ),
            Behavior(
                key=key('census_blockgroup'),
                parents=[get_behavior('census')],
                abstract=True
            ),
            Behavior(
                key=key('census_block'),
                parents=[get_behavior('census')],
                abstract=True
            ),
            Behavior(
                key=key('base_demographic'),
                parents=[get_behavior('base'), get_behavior('demographic')],
                abstract=True
            ),
            Behavior(
                key=key('base_agriculture'),
                parents=[get_behavior('base'), get_behavior('demographic')],
                abstract=True
            ),
            Behavior(
                key=key('vmt_future_trip_lengths'),
                parents=[get_behavior('future'), get_behavior('trips')],
                abstract=True
            ),
            Behavior(
                key=key('vmt_base_trip_lengths'),
                parents=[get_behavior('base'), get_behavior('trips')],
                abstract=True
            ),
            Behavior(
                key=key('climate_zones'),
                parents=[get_behavior('base'), get_behavior('climate')],
                intersection=Intersection(from_type='polygon', to_type='centroid'),
                abstract=True
            ),
            Behavior(
                key=key('existing_land_use'),
                parents=[get_behavior('base')],
                abstract=True
            ),
            # user_interface is a parent to behaviors that pertain only to the user interface
            Behavior(
                key=key('user_interface'),
                abstract=True
            ),
            # canvas describes the ability to paint a Feature table
            Behavior(
                key=key('canvas'),
                parents=[get_behavior('user_interface')]
            ),
            Behavior(
                key=key('future_scenario_feature'),
                parents=[get_behavior('future'), get_behavior('canvas')],
                abstract=True
            ),
            Behavior(
                key=key('future_developable'),
                parents=[get_behavior('future'), get_behavior('developable')],
                abstract=True
            ),
            Behavior(
                key=key('internal_analysis'),
                parents=[],
                abstract=True
            ),
            Behavior(
                key=key('end_state_demographic'),
                parents=[get_behavior('future_output'), get_behavior('demographic')],
                abstract=True
            ),
            Behavior(
                # Background imagery
                key=key('imagery'),
                parents=[],
                abstract=True
            ),
            Behavior(
                # Remote data sources
                key=key('remote'),
                parents=[],
                abstract=True
            ),
            Behavior(
                key=key('remote_imagery'),
                parents=[get_behavior('remote'), get_behavior('imagery')]
            ),
            Behavior(
                key=key('result'),
                abstract=True
            )
        ])
