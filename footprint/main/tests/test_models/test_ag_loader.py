import unittest
from footprint.main.data.load_ag_scenario_table import AgScenarioLoader

__author__ = 'calthorpe'

class TestSourceDataLoader(unittest.TestCase):

    def setUp(self):
        loader = AgScenarioLoader()

    def teardown(self):
        pass

    def test_ag_loader(self):

        AgScenarioLoader().load_project_to_source_db('sutter_county')
