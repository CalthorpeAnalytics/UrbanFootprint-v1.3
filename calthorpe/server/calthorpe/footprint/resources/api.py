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
import os
from settings import API_PATH

__author__ = 'calthorpe'

def detail_url(instance, format='json'):
    """
        Given a model instance returns the base tastypie API url
    :param instance: Any model instance supported by the API
    :return: the string URL
    """
    return os.path.join(API_PATH, instance.__class__._meta.verbose_name_raw, str(instance.pk), '?format={0}'.format(format))

def list_url(cls, format='json'):
    return os.path.join(API_PATH, cls._meta.verbose_name_raw, '?format={0}'.format(format))
