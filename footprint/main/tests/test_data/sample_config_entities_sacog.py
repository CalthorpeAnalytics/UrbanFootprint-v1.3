# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
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

__author__ = 'calthorpe_associates'

regions = [
    {
      'key': 'sacog',
      'name': 'SACOG',
      'description': 'The SACOG region',
      'bounds': MultiPolygon([Polygon(
    ((-122.719, 37.394), # bottom left
     (-122.719, 38.059), # top left
     (-121.603, 38.059), # top right
     (-121.603, 37.394), # bottom right
     (-122.719, 37.394), # bottom leftsample_config_entities
    ) )])
  },
]

projects = [
    {
        'key': 'saccity',
        'name': 'Sacramento City',
        'description': 'Sample project of the city of Sacramento',
        'base_year': 2013,
        'region_index':0,
        'bounds': MultiPolygon([Polygon(
            ((-122.719, 37.394), # bottom left
             (-122.719, 38.059), # top left
             (-121.603, 38.059), # top right
             (-121.603, 37.394), # bottom right
             (-122.719, 37.394), # bottom left
                ) )])
    },
    {
        'key': 'saccounty',
        'name':  'Sacramento County',
        'description':  "Sample project of the county of Sacramento",
        'base_year': 2013,
        'region_index':0,
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
        'key': 'smartcity',
        'name': 'Smart Growth Scenario',
        'description': 'Aggressive smart-growth scenario for city',
        'year': 2030,
        'project_index': 0,
        'selections': dict(built_form_sets='placetype'),
        'categories': [Category(key='category', value='smart'), Category(key='coastal', value='yes')]
    },
    {
        'key': 'trendcity',
        'name':  'Trend Scenario',
        'description': 'Business-as-usual scenario for city',
        'year': 2030,
        'project_index': 0,
        'selections': dict(built_form_sets='placetype'),
        'categories': [Category(key='category', value='trend'), Category(key='coastal', value='yes')]
    },
    {
        'key': 'greencity',
        'name':  'Green Scenario',
        'description': 'Green scenario for city',
        'year': 2030,
        'project_index': 0,
        'selections': dict(built_form_sets='placetype'),
        'categories': [Category(key='category', value='smart'), Category(key='coastal', value='yes')]
    },
    {
        'key': 'city',
        'name':  'Growth Scenario',
        'description': 'Business-as-usual growth scenario for city',
        'year': 2030,
        'project_index': 0,
        'selections': dict(built_form_sets='placetype'),
        'categories': [Category(key='category', value='trend'), Category(key='coastal', value='yes')]
    },
    {
        'key': 'smartcounty',
        'name': 'Smart Growth Scenario',
        'description': 'Aggressive smart-growth scenario for county',
        'year': 2030,
        'project_index': 1,
        'selections': dict(built_form_sets='placetype'),
        'categories': [Category(key='category', value='smart'), Category(key='coastal', value='no')]
    },
    {
        'key': 'trendcounty',
        'name':  'Trend Scenario',
        'description': 'Business-as-usual scenario fo city',
        'year': 2030,
        'project_index': 1,
        'selections': dict(built_form_sets='placetype'),
        'categories': [Category(key='category', value='trend'), Category(key='coastal', value='no')]
    }
]
