from footprint.client.configuration.fixture import ConfigEntitiesFixture
from footprint.main.models.category import Category
from footprint.main.models.config.scenario import BaseScenario, FutureScenario


__author__ = 'calthorpe_associates'


class ScagOrangeCountyConfigEntitiesFixture(ConfigEntitiesFixture):


    def scenarios(self, project=None, class_scope=None):

        parent_fixture = self.parent_fixture
        return self.matching_scope(parent_fixture.scenarios(project) + [
            {
                'class_scope': BaseScenario,
                'key': '{0}_base'.format(project.key.split('_')[0]),
                'name': '{0}'.format(project.name),
                'description': 'Base year data review and editing',
                'year': 2012,
                'selections': dict(built_form_sets='scag_land_use'),
                'categories': [Category(key='category', value='base_year')]
            },
            {
                'class_scope': FutureScenario,
                'key': '{0}_scenario_a'.format(project.key),
                'scope': project.schema(),
                'name': 'Scenario A',
                'description': 'Future Scenario for {0}'.format(project.name),
                'year': 2050,
                'selections': dict(),
                'categories': [Category(key='category', value='Future')]
            },
            {
                'class_scope': FutureScenario,
                'key': '{0}_scenario_b'.format(project.key),
                'scope': project.schema(),
                'name': 'Scenario B',
                'description': 'Future Scenario for {0}'.format(project.name),
                'year': 2050,
                'selections': dict(),
                'categories': [Category(key='category', value='Future')]
            }], project_key=project.key if project else None, class_scope=class_scope)


