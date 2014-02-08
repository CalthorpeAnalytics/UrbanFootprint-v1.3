from footprint.initialization.fixture import ConfigEntitiesFixture
from footprint.models.category import Category
from footprint.models.config.scenario import BaseScenario


__author__ = 'calthorpe'



class ScagIrvineConfigEntitiesFixture(ConfigEntitiesFixture):


    def scenarios(self, project=None, class_scope=None):

        parent_fixture = self.parent_fixture
        return self.matching_scope(parent_fixture.scenarios(project) + [
            {
                'class_scope': BaseScenario,
                'key': '{0}_base'.format(project.key.split('_')[0]),
                'name': '{0} Base'.format(project.name),
                'description': 'Base year parcel review and editing {0}'.format(project.name),
                'year': 2012,
                'selections': dict(built_form_sets='scag_land_use'),
                'categories': [Category(key='category', value='base_year')]
            }], project_key=project.key if project else None, class_scope=class_scope)


