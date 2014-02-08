__author__ = 'calthorpe'

from footprint.initialization.fixture import InitFixture

class SandagInitFixture(InitFixture):
    def import_database(self):
        return dict(
            host='10.0.0.133',
            database='sandag_urbanfootprint',
            user='calthorpe',
            password='Calthorpe123')
