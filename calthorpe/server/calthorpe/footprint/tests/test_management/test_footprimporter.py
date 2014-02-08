from django.core.management import call_command

__author__ = 'calthorpe'

import unittest
from nose import with_setup

class TestFootprimporter(unittest.TestCase):
    def test_import(self):
        call_command('footprimporter',
            schema='bayarea',
            host='10.0.0.133',
            user='calthorpe',
            password='Calthorpe123',
            database='uf_restore',
            test=True,
            footprintversion=0,
            base='grid150m_bayarea_loaded_census2010_placetyped')
