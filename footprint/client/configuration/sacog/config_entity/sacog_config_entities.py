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

            {
                'key': 'sutter_co',
                'import_key': 'sutter_county',
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
             #
             # {
             #     'key': 'sac_co',
             #     'import_key': 'sacramento_county',
             #     'name':  'Sacramento County',
             #     'description':  "Sacramento County",
             #     'base_year': 2013,
             #     'region_index': 0,
             #     'media': [],
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
        ]

    def scenarios(self, project=None, class_scope=None):
        return self.matching_scope([
            {
                'class_scope': BaseScenario,
                'key': 'base_condition',
                'scope': project.schema(),
                'name': 'Base Condition',
                'description': '{0} Base Scenario {1}'.format('2012', project.name),
                'year': 2012,
                'selections': dict(built_form_sets='sacog_building_type')
            },
            {
                'class_scope': FutureScenario,
                'key': 'scenario_a',
                'scope': project.schema(),
                'name': 'Scenario A',
                'description': 'Future Scenario for {0}'.format(project.name),
                'year': 2050,
                'selections': dict(built_form_sets='sacog_building_type')
            },
            {
                'class_scope': FutureScenario,
                'key': 'scenario_b',
                'scope': project.schema(),
                'name': 'Scenario B',
                'description': 'Future Scenario for {0}'.format(project.name),
                'year': 2050,
                'selections': dict(built_form_sets='sacog_building_type')
            }], project_key=project.key if project else None, class_scope=class_scope)

