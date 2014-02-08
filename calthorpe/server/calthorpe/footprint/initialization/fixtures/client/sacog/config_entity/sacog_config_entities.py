from footprint.initialization.fixture import ConfigEntitiesFixture, MediumFixture
from footprint.initialization.fixtures.client.default.config_entity.default_config_entities import ConfigEntityMediumKey
from footprint.models.category import Category
from footprint.models.config.scenario import BaseScenario, FutureScenario
from settings import CLIENT

__author__ = 'calthorpe'
from django.contrib.gis.geos import MultiPolygon, Polygon

__author__ = 'calthorpe'


class SacogConfigEntitiesFixture(ConfigEntitiesFixture):
    def project_key(self):
        return None

    def region_key(self):
        return 'sacog'

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
            # {
            #     'key': 'eldorado_county',
            #     'name':  'El Dorado County',
            #     'description':  "El Dorado County",
            #     'base_year': 2013,
            #     'region_index': 0,
            #     'bounds': MultiPolygon([Polygon(
            #         (
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #         )
            #     )])
            # },
            # {
            #     'key': 'placer_county',
            #     'name':  'Placer County',
            #     'description':  "Placer County",
            #     'base_year': 2013,
            #     'region_index': 0,
            #     'bounds': MultiPolygon([Polygon(
            #         (
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #         )
            #     )])
            # },
            {
                'key': 'sacramento_county',
                'name': 'Sacramento County',
                'description': "County of Sacramento",
                'base_year': 2013,
                'region_index': 0,
                'media': [
                    MediumFixture(self.schema, key=ConfigEntityMediumKey.Fab.ricate('irvine_logo'), name='Irvine Logo',
                                  url='/static/client/{0}/logos/cityofirvine.png'.format(CLIENT))
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
            # {
            #     'key': 'sutter_county',
            #     'name':  'Sutter County',
            #     'description':  "Sutter County",
            #     'base_year': 2013,
            #     'region_index': 0,
            #     'bounds': MultiPolygon([Polygon(
            #         (
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #         )
            #     )])
            # },
            # {
            #     'key': 'yolo_county',
            #     'name': 'Yolo County',
            #     'description': "Yolo County",
            #     'base_year': 2013,
            #     'region_index': 0,
            #     'bounds': MultiPolygon([Polygon(
            #         (
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #         )
            #     )])
            # }
            # {
            #     'key': 'yuba_county',
            #     'name':  'Yuba County',
            #     'description':  "Yuba County",
            #     'base_year': 2013,
            #     'region_index': 0,
            #     'bounds': MultiPolygon([Polygon(
            #         (
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #             (-121.738056, 38.553889),
            #         )
            #     )])
            # }
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

