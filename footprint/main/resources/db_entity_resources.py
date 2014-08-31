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
import re

from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.fields import ListField, ToOneField
from tastypie.resources import ModelResource

from footprint.main.lib.functions import remove_keys
from footprint.main.models.config.db_entity_interest import DbEntityInterest
from footprint.main.models.geospatial.db_entity import DbEntity
from footprint.main.models.config.interest import Interest
from footprint.main.resources.behavior_resources import FeatureBehaviorResource
from footprint.main.resources.config_entity_resources import ConfigEntityResource
from footprint.main.resources.mixins.mixins import TagResourceMixin, TimestampResourceMixin, CloneableResourceMixin
from footprint.main.resources.footprint_resource import FootprintResource
from footprint.main.resources.pickled_dict_field import PickledDictField

__author__ = 'calthorpe_associates'

class DbEntityResource(FootprintResource, TagResourceMixin, TimestampResourceMixin, CloneableResourceMixin):
    hosts = fields.ListField('hosts', null=True)

    # This gets sent by the client and is used to set the url.
    # It is marked readonly so that tastypie doesn't try to find a matching
    # DbEntity attribute using it. I don't know how to tell tastypie to just map this
    # value to url
    upload_id = fields.CharField(null=True, readonly=True)

    # FeatureClassConfiguration isn't a model class, so we just pickle it
    feature_class_configuration = PickledDictField(attribute='feature_class_configuration_as_dict', null=True)

    # FeatureBehavior is a settable property of DbEntity, since the relationship is actually defined from FeatureBehavior to DbEntity.
    feature_behavior = ToOneField(FeatureBehaviorResource, attribute='feature_behavior', null=True, full=True)

    @staticmethod
    def increment_key(key):
        r = r'_(\d+)$'
        m = r.match(key)
        if m:
            replacement = '_%s' % int(m.group(1))+1
            return re.sub(replacement, key)

    def lookup_kwargs_with_identifiers(self, bundle, kwargs):
        """
            Override to remove feature_behavior from the lookup_kwargs,
            since it is actually defined in reverse--feature_behavior has a db_entity
        """
        return remove_keys(
            super(DbEntityResource, self).lookup_kwargs_with_identifiers(bundle, kwargs),
            ['feature_behavior'])

    def hydrate(self, bundle):
        if not bundle.data.get('id'):
            bundle.obj.creator = self.resolve_user(bundle.request.GET)
            # Update the key if this is a new instance but the key already is in use
            while DbEntity.objects.filter(key=bundle.obj.key).count() > 0:
                bundle.obj.key = self.increment_key(bundle.obj.key)
        else:
            # Set the back-reference to the db_entity
            # We have to load form the db since bundle.obj isn't yet hydrated
            temp_bundle = self.build_bundle(obj=DbEntity.objects.get(id=bundle.data['id']))
            bundle.data['feature_behavior']['db_entity'] = self.get_resource_uri(temp_bundle)

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
        excludes=['table', 'query', 'hosts', 'group_by']
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

    def full_hydrate(self, bundle):
        hydrated_bundle = super(DbEntityInterestResource, self).full_hydrate(bundle)
        # If new, Ensure the db_entity schema matches that of the config_entity
        # This happens after all hydration since it depends on two different fields
        if not hydrated_bundle.obj.id:
            hydrated_bundle.obj.db_entity.schema = hydrated_bundle.obj.config_entity.schema()
        return hydrated_bundle

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = DbEntityInterest.objects.filter(deleted=False)
        resource_name= 'db_entity_interest'

