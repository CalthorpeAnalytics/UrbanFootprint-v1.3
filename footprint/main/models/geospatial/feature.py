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
import logging
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.db.models import GeoManager
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.mixins.timestamps import Timestamps
from footprint.main.models.analysis_module.analysis_module import AnalysisModule
logger = logging.getLogger(__name__)

__author__ = 'calthorpe_associates'

class Feature(models.Model):
    """
        A mixin model class that references a Geography instance. The abstract Geography class and its subclasses
        represent geography authorities, so that any shared geographies like regional parcels have one authoritive
        locations. Derived classes and their instances, such as the ConfigEntityGeography derivative classes use the
        Geographic mixin to reference the authoritative geographies of the Geography class hierarchy
    """
    # Base manager inherited by subclasses
    objects = GeoManager()

    # The geometry imported for the feature
    wkb_geometry = models.GeometryField()

    api_include=None

    @classmethod
    def limited_api_fields(cls):
        return ['id']+cls.api_include if cls.api_include else None


    # I don't know why this was ever in here
    # def __getattribute__(self, name):
    #     """
    #     Override that, if an attribute isn't found on the object, then it instead
    #     looks for the same attribute prefixed with 'temp_' and tries to return
    #     that value.
    #     """
    #
    #     try:
    #         return object.__getattribute__(self, name)
    #     except AttributeError:
    #         if '_id' in name:
    #             temp_name = name.replace('_id', '')
    #             return object.__getattribute__(self, temp_name)[0].id
    #         else:
    #             temp_name = '{0}s'.format(name)
    #             return object.__getattribute__(self, temp_name)[0]

    def save(self, force_insert=False, force_update=False, using=None):
        # On update, make sure created is never set to null
        # This is a stupid Tastypie problem
        if self.id and not self.created:
            self.created = self.__class__.objects.get(id=self.id).created
        super(Feature, self).save(force_insert, force_update, using)

    @classmethod
    def post_save(cls, user_id, objects, **kwargs):
        """
            Optional class method to kick of analytic modules (see FutureScenarioFeature)
        """
        pass

    class Meta(object):
        abstract = True
        app_label='main'

class UpdatingFeature(Feature, Timestamps):
    objects = GeoManager()

    @classmethod
    def limited_api_fields(cls):
        return ['id', 'updated']+cls.api_include if cls.api_include else None

    class Meta(object):
        abstract = True
        app_label = 'main'


class PaintingFeature(UpdatingFeature):
    objects = GeoManager()

    dev_pct = models.DecimalField(max_digits=8, decimal_places=4, default=1.0000)
    density_pct = models.DecimalField(max_digits=8, decimal_places=4, default=1.0000)
    gross_net_pct = models.DecimalField(max_digits=8, decimal_places=4, default=1.0000)
    dirty_flag = models.BooleanField(default=False)

    @classmethod
    def post_save(cls, user_id, objects, **kwargs):
        from footprint.main.models.analysis_module.analysis_module import AnalysisModuleKey
        core = AnalysisModule.objects.get(config_entity=cls.config_entity, key=AnalysisModuleKey.SCENARIO_BUILDER)
        # Update the core user to the current user
        if not core.updater or core.updater.id != user_id:
            core.updater = User.objects.get(id=user_id)
            core._no_post_save_task_run = True
            core.save()
            core._no_post_save_task_run = False
        ids = map(lambda obj: obj.id, objects)
        # logger.debug("Calling Scenario Builder on Scenario %s to update features: %s" % (cls.config_entity, ', '.join(ids)))
        core.start(ids=ids)

    class Meta(object):
        abstract = True
        app_label = 'main'


class FeatureGeography(models.Model):
    """
    An abstract class representing the association between a Feature class and Geography class
    """
    objects = GeoInheritanceManager()

    # Associates a Feature class to a Geography class
    # Assign these to ForeignKey fields
    feature = None
    geography = None

    def __unicode__(self):
        return "FeatureGeography:Feature:{1}, Geography:{2}".format(self.feature, self.geography)
    class Meta(object):
        app_label = 'main'
        abstract = True
