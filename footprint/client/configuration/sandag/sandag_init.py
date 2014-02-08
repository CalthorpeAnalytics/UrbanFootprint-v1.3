__author__ = 'calthorpe_associates'

from footprint.client.configuration.fixture import InitFixture

class SandagInitFixture(InitFixture):
    def import_database(self):
        return dict(
            host='10.0.0.133',
            database='urbanfootprint_dev',
            user='footprint',
            password='[PASSWORD]')
