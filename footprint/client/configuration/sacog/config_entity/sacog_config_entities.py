from footprint.client.configuration.fixture import ConfigEntitiesFixture
from footprint.main.models.category import Category
from footprint.main.models.config.scenario import BaseScenario, FutureScenario

__author__ = 'calthorpe_associates'
from django.contrib.gis.geos import MultiPolygon, Polygon

__author__ = 'calthorpe_associates'


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
            #     'key': 'sacramento_county',
            #     'name': 'Sacramento County',
            #     'description': "County of Sacramento",
            #     'base_year': 2013,
            #     'region_index': 0,
            #     'media': [
            #         MediumFixture(self.schema, key=ConfigEntityMediumKey.Fab.ricate('irvine_logo'), name='Irvine Logo',
            #                       url='/static/client/{0}/logos/cityofirvine.png'.format(CLIENT))
            #     ],
            #     'bounds': MultiPolygon([Polygon(
            #         (
            #             # Sacramento County bounds
            #             (-121.862622000787, 38.018420999589), # bottom left
            #             (-121.862622000787, 38.7364049988308), # top left
            #             (-121.027084001338, 38.7364049988308), # top right
            #             (-121.027084001338, 38.018420999589), # top right
            #             (-121.862622000787, 38.018420999589)  # bottom left
            #         )
            #     )])
            # }
            {
                'key': 'sutter_county',
                'name':  'Sutter County',
                'description':  "Sutter County",
                'base_year': 2013,
                'region_index': 0,
                'media': [],
                'bounds': MultiPolygon([Polygon(
                    (
                        (-121.738056, 38.553889),
                        (-121.738056, 38.553889),
                        (-121.738056, 38.553889),
                        (-121.738056, 38.553889),
                        (-121.738056, 38.553889),
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
                'key': '{0}_scenario_a'.format(project.key),
                'scope': project.schema(),
                'name': 'Scenario A',
                'description': 'Future Scenario for {0}'.format(project.name),
                'year': 2050,
                'selections': dict(built_form_sets='sacog_buildingtypes'),
                'categories': [Category(key='category', value='Future')]
            },
            {
                'class_scope': FutureScenario,
                'key': '{0}_scenario_b'.format(project.key),
                'scope': project.schema(),
                'name': 'Scenario B',
                'description': 'Future Scenario for {0}'.format(project.name),
                'year': 2050,
                'selections': dict(built_form_sets='sacog_buildingtypes'),
                'categories': [Category(key='category', value='Future')]
            }], project_key=project.key if project else None, class_scope=class_scope)

