from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager

__author__ = 'calthorpe_associates'
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

from django.db import models
from picklefield import PickledObjectField

class TileStacheLayer(models.Model):
    """
        Key-value pairs for the TileStacheConfig.config instance
    """
    # The layer key
    key = models.CharField(max_length=200)
    # A pickled Tilestache CoreLayer
    value = PickledObjectField()

    class Meta(object):
        app_label = 'main'

class TileStacheConfig(models.Model):
    """
        Represents the TileStache config dictionary, stored in the config field
    """
    objects = GeoInheritanceManager()
    name = models.CharField(max_length=50, default='default')
    # A TileStache.Config.Configuration instance
    config = PickledObjectField()
    # These layers are used to create the config.
    # They are manyToMany so that multiple processes can write layers without overwriting each other when they save the config
    layers = models.ManyToManyField(TileStacheLayer)
    enable_caching = models.NullBooleanField(default=True)

    class Meta(object):
        app_label = 'main'

