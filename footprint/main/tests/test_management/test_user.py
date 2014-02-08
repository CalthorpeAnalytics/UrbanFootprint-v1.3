from django.utils import unittest
from footprint.main.initialization.data_provider import DataProvider
from nose.tools import assert_equal

__author__ = 'calthorpe_associates'

class TestUser(unittest.TestCase):
    def test_add_user(self):
        results = DataProvider().user('testy', 'testy', 'test@test.test', 'TEST_API_KEY')
        user = results['user']
        api_key = results['api_key']
        assert_equal(user.username, 'testy')
        assert_equal(user.email, 'test@test.test')
        assert_equal(api_key.key, 'TEST_API_KEY')
