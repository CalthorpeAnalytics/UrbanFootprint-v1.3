# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
 # GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com
from django.contrib.gis.geos import MultiPolygon, Polygon
from footprint.main.mixins.category import Category
from django.conf import settings
__author__ = 'calthorpe_associates'

regions = [
    {
      'key': 'eastbaywest',
      'name': 'East Bay West',
      'description': 'Alameda is possibly the best county in the Bay Area. It contains sweeping vistas, intellectual firepower, and hip culture',
      'bounds': MultiPolygon([Polygon(
    ((-122.719, 37.394), # bottom left
     (-122.719, 38.059), # top left
     (-121.603, 38.059), # top right
     (-121.603, 37.394), # bottom right
     (-122.719, 37.394), # bottom left
    ) )])
  },
  {
      'key': 'eastbayeast',
      'name':  'East Bay East',
      'description':  "Contra Costa county is so named for its juxtaposition with San Francisco",
      'bounds': MultiPolygon([Polygon(
    ((-122.4319, 37.7182), # bottom left
     (-122.4319, 38.1002), # top left
     (-121.5356, 38.1002), # top right
     (-121.5356, 37.7182), # bottom right
     (-122.4319, 37.7182), # bottom left
     ) )])
  }
]

projects = [
    {
        'key': 'alameda',
        'name': 'Alameda County',
        'description': 'This project is aimed at making Alameda county event cooler',
        'base_table': settings.STATIC_ROOT + 'sample_data/eastbaywest_alameda_base',

        'base_year': 2012,
        'region_index': 0,
        'bounds': MultiPolygon([Polygon(
            ((-122.719, 37.394), # bottom left
             (-122.719, 38.059), # top left
             (-121.603, 38.059), # top right
             (-121.603, 37.394), # bottom right
             (-122.719, 37.394), # bottom left
                ) )])
    },
    {
        'key': 'contracosta',
        'name':  'Contra Costa County',
        'description':  "This project intents to explore densification options around the county's train stations",
        'base_year': 2012,
        'region_index': 1,
        'bounds': MultiPolygon([Polygon(
            ((-122.4319, 37.7182), # bottom left
             (-122.4319, 38.1002), # top left
             (-121.5356, 38.1002), # top right
             (-121.5356, 37.7182), # bottom right
             (-122.4319, 37.7182), # bottom left
                ) )])
    }
]

scenarios = [
    {
        'key': 'smart',
        'name': 'Smart Growth Scenario',
        'description': 'This scenario is aimed at making Alameda county grow up smart',
        'year': 2030,
        'project_index': 0,
        'categories': [Category(key='category', value='smart'), Category(key='coastal', value='yes')]
    },
    {
        'key': 'trend',
        'name':  'Trend Scenario',
        'description': "This business as usual scenario is Alameda county's road to mediocrity",
        'year': 2030,
        'project_index': 0,
        'categories': [Category(key='category', value='dumb'), Category(key='coastal', value='yes')]
    },
    {
        'key': 'smart_cc',
        'name': 'Smart Growth Scenario',
        'description': 'This scenario is aimed at making Contra Costa county grow up smart',
        'year': 2030,
        'project_index': 1,
        'categories': [Category(key='category', value='smart'), Category(key='coastal', value='no')]
    },
    {
        'key': 'trend_cc',
        'name':  'Trend Scenario',
        'description': "This business as usual scenario is Contra Costa's road to mediocrity",
        'year': 2030,
        'project_index': 1,
        'categories': [Category(key='category', value='dumb'), Category(key='coastal', value='no')]
    }
]
