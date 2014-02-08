from footprint.initialization.fixture import ConfigEntitiesFixture, MediumFixture
from footprint.initialization.fixtures.client.default.config_entity.default_config_entities import ConfigEntityMediumKey
from footprint.lib.functions import flatten
from footprint.models.config.scenario import BaseScenario, FutureScenario
from settings import CLIENT

__author__ = 'calthorpe'
from django.contrib.gis.geos import MultiPolygon, Polygon
from footprint.mixins.category import Category

__author__ = 'calthorpe'


class DemoConfigEntitiesFixture(ConfigEntitiesFixture):
    def regions(self):
        return [
            {
                'key': 'sacog',
                'name': 'SACOG',
                'description': 'The SACOG region',
                'bounds': MultiPolygon([Polygon((
                    (-122.719, 37.394),  # bottom left
                    (-122.719, 38.059),  # top left
                    (-121.603, 38.059),  # top right
                    (-121.603, 37.394),  # bottom right
                    (-122.719, 37.394),  # bottom leftsample_config_entities
                ))])
            },
        ]

    def projects(self, region=None):
        return [
            {
                'key': 'city_of_sacramento',
                'name': 'Sacramento',
                'description': "City of Sacramento",
                'base_year': 2013,
                'region_index': 0,
                'media': [
                    MediumFixture(key=ConfigEntityMediumKey.Fab.ricate('irvine_logo'), name='Irvine Logo',
                                  url='/static/client/{0}/logos/cityofsacramento.png'.format(CLIENT))
                ],
                'bounds': MultiPolygon([Polygon(
                    (
                        # Sacramento County bounds
                        (-121.862622000787, 38.018420999589), # bottom left
                        (-121.862622000787, 38.7364049988308), # top left
                        (-121.027084001338, 38.7364049988308), # top right
                        (-121.027084001338, 38.018420999589), # top right
                        (-121.862622000787, 38.018420999589)  # bottom left
                    )
                )])
            }
        ]

    def scenarios(self, project=None, class_scope=None):
        return self.matching_scope([
            {
                'class_scope': BaseScenario,
                'key': '{0}_base'.format(project.key),
                'scope': project.schema(),
                'name': 'Base',
                'description': '{0} Base Scenario {1}'.format('2012', project.name),
                'year': 2012,
                'selections': dict(built_form_sets='sacog_buildingtypes'),
                'categories': [Category(key='category', value='Base')]
            },
            {
                'class_scope': FutureScenario,
                'key': '{0}_compact'.format(project.key),
                'scope': project.schema(),
                'name': 'Compact',
                'description': '{0} Compact Future Scenario for {1}'.format('2040', project.name),
                'year': 2040,
                'selections': dict(built_form_sets='sacog_buildingtypes'),
                'categories': [Category(key='category', value='Future')]
            },
            {
                'class_scope': FutureScenario,
                'key': '{0}_trend'.format(project.key),
                'scope': project.schema(),
                'name': 'Trend'.format(project.name),
                'description': '{0} Trend Future Scenario for {1}'.format('2040', project.name),
                'year': 2040,
                'selections': dict(built_form_sets='sacog_buildingtypes'),
                'categories': [Category(key='category', value='Future')]
            }
        ], project_key=project.key if project else None, class_scope=class_scope)

