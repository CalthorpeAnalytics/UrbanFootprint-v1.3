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
from contextlib import contextmanager
from django.db import models
from footprint.main.managers.config.db_entity_interest_manager import DbEntityInterestManager
from footprint.main.mixins.deletable import Deletable
from footprint.main.mixins.post_save_publishing import PostSavePublishing
from footprint.main.models.geospatial.db_entity import DbEntity
from footprint.main.models.config.interest import Interest
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator

__author__ = 'calthorpe_associates'

class DbEntityInterest(Deletable):
    objects = DbEntityInterestManager()

    # A class name is used to avoid circular dependency
    config_entity = models.ForeignKey('ConfigEntity', null=False)
    db_entity = models.ForeignKey(DbEntity, null=False)
    interest = models.ForeignKey(Interest, null=False)
    _no_post_save_publishing = False

    @property
    def feature_fields(self):
        """
            The fields of the DbEntity's Feature class, if one exists
        """
        feature_class_creator = FeatureClassCreator(self.config_entity, self.db_entity)
        if not feature_class_creator.dynamic_model_class_is_ready:
            return []
        feature_class = feature_class_creator.dynamic_model_class()
        return feature_class_creator.dynamic_model_class().objects.all().result_fields_and_title_lookup()[0] if feature_class else []

    @property
    def feature_field_title_lookup(self):
        """
            The fields to title lookup of the DbEntity's Feature class, if one exists
        """
        feature_class_creator = FeatureClassCreator(self.config_entity, self.db_entity)
        if not feature_class_creator.dynamic_model_class_is_ready:
            return {}
        feature_class = feature_class_creator.dynamic_model_class()
        return feature_class_creator.dynamic_model_class().objects.all().result_fields_and_title_lookup()[1] if feature_class else {}

    def __unicode__(self):
        return "ConfigEntity:{0}, DbEntity:{1}, Interest:{2}".format(self.config_entity, self.db_entity, self.interest)

    class Meta(object):
        app_label = 'main'
