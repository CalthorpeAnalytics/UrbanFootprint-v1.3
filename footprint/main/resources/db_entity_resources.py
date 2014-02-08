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
from django.conf.urls import url

from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.fields import ListField, ToOneField
from tastypie.resources import ModelResource
from footprint.main.models.config.db_entity_interest import DbEntityInterest
from footprint.main.models.geospatial.db_entity import DbEntity
from footprint.main.models.config.interest import Interest
from footprint.main.resources.config_entity_resources import ConfigEntityResource
from footprint.main.resources.mixins.mixins import TagResourceMixin
from footprint.main.resources.footprint_resource import FootprintResource
from footprint.main.resources.pickled_dict_field import PickledDictField

__author__ = 'calthorpe_associates'

class DbEntityResource(FootprintResource, TagResourceMixin):
    hosts = fields.ListField('hosts', null=True)

    # This gets sent by the client and is used to set the url.
    # It is marked readonly so that tastypie doesn't try to find a matching
    # DbEntity using it. I don't know how to tell tastypie to just map this
    # value to url
    upload_id = fields.CharField(null=True, readonly=True)
    origin_instance = ToOneField('self', attribute='origin_instance', null=True)

    def hydrate(self, bundle):
        if not bundle.obj.id:
            bundle.obj.creator = self.resolve_user(bundle.request.GET)
        bundle.obj.updater = self.resolve_user(bundle.request.GET)
        return bundle

    def hydrate_url(self, bundle):
        # Use the upload_id to create a source url for the db_entity
        if bundle.data.get('upload_id', False):
            bundle.data['url'] = 'file:///tmp/%s' % bundle.data['upload_id']
        return bundle

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = DbEntity.objects.filter(deleted=False)
        excludes=['feature_class_configuration']
        resource_name= 'db_entity'

class InterestResource(ModelResource):
    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = Interest.objects.all()

class DbEntityInterestResource(ModelResource):
    config_entity = fields.ToOneField(ConfigEntityResource, 'config_entity', full=False)
    db_entity = fields.ToOneField(DbEntityResource, 'db_entity', full=True)
    interest = fields.ToOneField(InterestResource, 'interest', full=True)

    # The fields of the DbEntity's feature class, if one exists
    feature_fields = ListField(attribute='feature_fields', null=True, blank=True, readonly=True)
    feature_field_title_lookup = PickledDictField(attribute='feature_field_title_lookup', null=True, blank=True, readonly=True)


    def dehydrate_interest(self, bundle):
        """
            Expose only the Interest.key via the API. This should be sufficient for the time being
        :param bundle:
        :return:
        """
        return bundle.data['interest'].data['key']

    def hydrate_interest(self, bundle):
        """
            Expect only the key of Interest in as the bundle.data['interest']
        :param bundle:
        :return:
        """
        interest_resource = InterestResource()
        if not isinstance(bundle.data['interest'], Bundle):
            # For some reason the interest sometimes comes in as a bundle, at least in testing
            interest = Interest.objects.get(key=bundle.data['interest'])
            bundle.data['interest'] = interest_resource.full_dehydrate(interest_resource.build_bundle(obj=interest))
        return bundle

    class Meta(FootprintResource.Meta):
        queryset = DbEntityInterest.objects.filter(deleted=False)
        resource_name= 'db_entity_interest'
