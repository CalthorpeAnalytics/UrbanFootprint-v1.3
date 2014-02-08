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
from django.contrib.auth import authenticate
from tastypie import fields
from tastypie.exceptions import NotFound

__author__ = 'calthorpe'

from tastypie.models import create_api_key, ApiKey
from django.db import models
from django.contrib.auth.models import User
from tastypie.authentication import ApiKeyAuthentication, BasicAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource

class ApiKeyResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = ApiKey.objects.all()
        resource_name = 'api_key'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()

class UserAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        params = request.GET
        if params.get('username', None) and params.get('password', None):
            username = params['username']
            password = params['password']
            return authenticate(username=username, password=password) is not None
        elif params.get('api_key', None):
            return len(User.objects.filter(api_key__key=params['api_key'])) == 1

    # Optional but recommended
    def get_identifier(self, request):
        return request.GET.get('username', None)

class UserResource(ModelResource):

    # Include the ApiKey so that the user can make authenticated calls
    api_key = fields.ToOneField(ApiKeyResource, 'api_key', full=True)

    def dehydrate_api_key(self, bundle):
        """
            Expose only the ApiKey.key via the API.
        :param bundle:
        :return:
        """
        return bundle.data['api_key'].data['key']

    def hydrate_api_key(self, bundle):
        """
            Convert the api key into a full instance if it matches
        :param bundle:
        :return:
        """
        try:
            bundle.obj.api_key = ApiKey.objects.filter(key=bundle.data['api_key'])
        except NotFound:
            bundle.obj.api_key = None
        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(UserResource, self).build_filters(filters)

        if orm_filters.get('password__exact', None):
            orm_filters.pop('password__exact')
        if "api_key__exact" in orm_filters:
            if orm_filters['api_key__exact']:
                orm_filters['api_key__key__exact'] = orm_filters['api_key__exact']
            orm_filters.pop('api_key__exact')

        return orm_filters

    class Meta:
        filtering = {
            "id": ('exact',),
            "username": ('exact',),
            "password": ('exact',),
            "api_key": ('exact',),
        }
        always_return_data = True
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['is_superuser', 'is_staff', 'last_login', 'date_joined']
        authentication = UserAuthentication()
        authorization = DjangoAuthorization()

models.signals.post_save.connect(create_api_key, sender=User)

class ApiTokenResource(ModelResource):
    class Meta(object):
        queryset = ApiKey.objects.all()
        resource_name = "token"
        include_resource_uri = False
        fields = ["key"]
        list_allowed_methods = []
        detail_allowed_methods = ["get"]
        authentication = BasicAuthentication()

    def obj_get(self, request=None, **kwargs):
        if kwargs["pk"] != "auth":
            raise NotImplementedError("Resource not found")

        user = request.user
        if not user.is_active:
            raise NotFound("User not active")

        api_key = ApiKey.objects.get(user=request.user)
        return api_key
