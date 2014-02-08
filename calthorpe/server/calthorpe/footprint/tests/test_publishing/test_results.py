from django.utils import unittest
from nose import with_setup
from footprint.initialization.data_provider import DataProvider


class TestResults(unittest.TestCase):
    """
    The TileStache classes will observe the layer library and the standard list of scenarios, and keep a
    config string to render all of the possible tables when they are requested. These tests make sure that
    system is working properly.
    :return:
    """

    def setup(self):
        pass

    def teardown(self):
        pass


    @with_setup(setup, teardown)
    def test_create_results(self):
        """
        :return:
        """

        scenario = DataProvider().scenarios()[0]
        scenario.save()

