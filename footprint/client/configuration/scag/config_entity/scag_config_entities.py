from footprint.client.configuration.fixture import ConfigEntitiesFixture, MediumFixture
from footprint.client.configuration.default.config_entity.default_config_entities import ConfigEntityMediumKey
from django.conf import settings

__author__ = 'calthorpe_associates'
from django.contrib.gis.geos import MultiPolygon, Polygon


class ScagConfigEntitiesFixture(ConfigEntitiesFixture):
    def project_key(self):
        return None

    def region_key(self):
        return 'scag'

    def regions(self):
        return [
            {
                'key': 'scag',
                'name': 'SCAG',
                'description': 'The SCAG region',
                'media': [
                    MediumFixture(key=ConfigEntityMediumKey.Fab.ricate('scag_logo'), name='SCAG Logo',
                                    url='/static/client/{0}/logos/scag.png'.format(CLIENT))
              ],
                #defaulting to an Irvine view for the moment
                'bounds': MultiPolygon([Polygon((
                    (-117.869537353516, 33.5993881225586),
                    (-117.869537353516, 33.7736549377441),
                    (-117.678024291992, 33.7736549377441),
                    (-117.678024291992, 33.5993881225586),
                    (-117.869537353516, 33.5993881225586),
                ))])

            },
        ]

    def projects(self, region=None):
        return [
            {
                'key': 'irvine',
                'name': 'Irvine',
                'description': "City of Irvine",
                'base_year': 2012,
                'region_index': 0,
                'media': [
                    MediumFixture(key=ConfigEntityMediumKey.Fab.ricate('irvine_logo'), name='Irvine Logo',
                                  url='/static/client/{0}/logos/cityofirvine.png'.format(settings.CLIENT))
                ],
                'bounds': MultiPolygon([Polygon((
                    (-117.869537353516, 33.5993881225586),
                    (-117.869537353516, 33.7736549377441),
                    (-117.678024291992, 33.7736549377441),
                    (-117.678024291992, 33.5993881225586),
                    (-117.869537353516, 33.5993881225586),
                ))])
            },
            {
                 'key': 'orange_county',
                 'name': 'Orange County',
                 'description': "City of Irvine",
                 'base_year': 2012,
                 'region_index': 0,
                 'media': [],
                 'bounds': MultiPolygon([Polygon((
                     (-117.869537353516, 33.5993881225586),
                     (-117.869537353516, 33.7736549377441),
                     (-117.678024291992, 33.7736549377441),
                     (-117.678024291992, 33.5993881225586),
                     (-117.869537353516, 33.5993881225586),
                 ))])
            }
        ]

    def scenarios(self, project=None, class_scope=None):
        return self.matching_scope([], project_key=project.key if project else None, class_scope=class_scope)


