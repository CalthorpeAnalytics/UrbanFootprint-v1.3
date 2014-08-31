import logging
from footprint.main.models import AnalysisModule

__author__ = 'calthorpe'
# coding=utf-8
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
from django.contrib.auth.models import User
from django.db import models
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.geospatial.feature import PaintingFeature
logger = logging.getLogger(__name__)

__author__ = 'calthorpe_associates'

class AgricultureFeature(PaintingFeature):
    """
    A dynamically subclassed abstract class that represents the agriculture canvas table for a specific Scenerio.
    Hence instances of subclasses of this class correspond to geography rows of the canvas table
    """
    objects = GeoInheritanceManager()

    built_form_key = models.CharField(max_length=100, default=None, null=True)
    crop_yield = models.FloatField(default=0)
    market_value = models.FloatField(default=0)
    production_cost = models.FloatField(default=0)
    water_consumption = models.FloatField(default=0)
    labor_force = models.FloatField(default=0)
    truck_trips = models.FloatField(default=0)

    @classmethod
    def post_save(cls, user_id, objects, **kwargs):
        ids = map(lambda obj: obj.id, objects)

        logger.info("Calling Agriculture Module on Scenario %s to update %s features" % (cls.config_entity, len(ids)))

        from footprint.main.models.analysis_module.analysis_module import AnalysisModuleKey
        analysis_module = AnalysisModule.objects.get(
            config_entity=cls.config_entity,
            key=AnalysisModuleKey.AGRICULTURE)
        # Update the core user to the current user
        if not analysis_module.updater or analysis_module.updater.id != user_id:
            analysis_module._no_post_save_publishing = True
            analysis_module.updater = User.objects.get(id=user_id)
            analysis_module._no_post_save_publishing = False
            analysis_module.save()
        # logger.debug("Calling Agriculture Module on Scenario %s to update features: %s" % (cls.config_entity, ', '.join(ids)))
        # TODO ids aren't yet being used by the module. They should be
        analysis_module.start(ids=ids)

    class Meta(object):
        app_label = 'main'
        abstract = True
