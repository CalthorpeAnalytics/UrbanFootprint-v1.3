from footprint.initialization.fixture import ProjectFixture
from footprint.lib.functions import merge

__author__ = 'calthorpe'


class ScagOrangeCountyProjectFixture(ProjectFixture):
    def feature_class_lookup(self):
        """
            Adds mappings of custom Feature classes
        :return:
        """
        parent_fixture = self.parent_fixture
        feature_class_lookup = parent_fixture.feature_class_lookup()
        return merge(feature_class_lookup, {})

    def default_db_entity_setups(self):
        """
            Project specific SCAG additional db_entities
        :param default_dict:
        :return:
        """
        return super(ScagOrangeCountyProjectFixture, self).default_db_entity_setups() + []
