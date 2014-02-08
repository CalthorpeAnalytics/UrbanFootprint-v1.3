import logging
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from inflection import singularize
from tastypie.authentication import ApiKeyAuthentication
from tastypie.exceptions import BadRequest
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.http import HttpBadRequest
from tastypie.resources import csrf_exempt
import traceback
from footprint.main.lib.functions import map_dict_to_dict, merge
from footprint.main.utils.dynamic_subclassing import get_dynamic_resource_class
from footprint.main.utils.subclasses import match_subclasses
from footprint.main.utils.utils import get_one_or, clear_many_cache
import json

__author__ = 'calthorpe_associates'

class FootprintResource(ModelResource):
    """
        Adds django revision with the tastypie ModelResource
    """
    def __init__(self):
        # Get an instance of a logger
        self.logger = logging.getLogger(__name__)
        super(FootprintResource, self).__init__()

    class Meta(object):
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()

    # From http://django-tastypie.readthedocs.org/en/latest/cookbook.html
    def dispatch(self, request_type, request, **kwargs):
        format = request.META.get('CONTENT_TYPE', 'application/json')
        # We only can log the raw_post_data if the request isn't multipart
        self.logger.debug(
            '%s %s %s' %
            (request.method, request.get_full_path(),
             request.raw_post_data if not format.startswith('multipart') else '...MULTIPART...'
            )
        )

        exception = None
        try:
            response = super(ModelResource, self).dispatch(
                request_type, request, **kwargs)

            if request.method in ['POST', 'PATCH']:
                self.post_save(request, **kwargs)
        except (BadRequest, fields.ApiFieldError), e:
            exception = e
            self.logger.debug(
                'Response 400 %s' % e.args[0])
            raise
        except ValidationError, e:
            exception = e
            self.logger.debug(
                'Response 400 %s' % e.messages)
            raise
        except Exception, e:
            exception = e
            if hasattr(e, 'response'):
                self.logger.debug(
                    'Response %s %s %s' %
                    (e.response.status_code, e.response.content, traceback.format_exc()))
            else:
                self.logger.debug('Response 500: %s' % e.message)
            raise
        # finally:
        #     if exception:
        #         bundle = dict(code=777, status=False, error=json.loads(
        #             merge(dict(content=exception.response.content) if hasattr(exception, 'response') else {}, dict(message=exception.message))))
        #         return self.create_response(request, bundle, response_class=HttpBadRequest)

        self.logger.debug(
            'Response %s %s' % (response.status_code, response.content))
        return response

    def wrap_view(self, view):
        """
            Overrides wrap_view to allow processing of dynamic resource classes. Special parameters such as config_entity_id are used to resolve the correct resource subclass.
        :param view:
        :return:
        """
        @csrf_exempt
        def wrapper(request, *args, **kwargs):
            # Dynamic resources based on a ConfigEntity instance need to pass the config_entity__id so that we can properly construct the dynamic resource
            if hasattr(self.Meta, 'abstract') and self.Meta.abstract:
                wrapped_view = self.subclass_resource_if_needed(view, request)
                # Preserve the original request parameters
                kwargs['GET'] = request.GET
                request.GET = request._filters if hasattr(request, '_filters') and len(request._filters.keys()) > 0 else request.GET
            else:
                wrapped_view = super(ModelResource, self).wrap_view(view)

            return wrapped_view(request, *args, **kwargs)
        return wrapper

    def subclass_resource_if_needed(self, view, request):
        """
            Called to dynamically subclass abstract resources that wrap dynamic model classes, such as abstract subclasses of Feature. The subclassing happens if the current resource class (self) is a subclass of DynamicResource and self is abstract, the latter needed to prevent infinite recursion. The subclassed resource wraps the view and thus becomes the resource executing the request

        :param request: The request with certain required parameters in GET. Important parameters are config_entity, which is a ConfigEntity id and layer, which is a Layer id. If a ConfigEntity id is given an the resource is a FeatureResource subclass, then a ConfigEntity-specific dynamic subclass is found
        :return: The wrapped view of the dynamic resource class instance or simply the wrapped view of self if no dynamic subclassing is needed.
        """

        # By default don't subclass, just call the super class wrap_view on the existing view
        return super(ModelResource, self).wrap_view(view)

    def post_save(self, request, **kwargs):
        """
            Optional operations to perform after POST, PUT, and PATCH
        :param request:
        :return:
        """
        pass

    def resolve_user(self, params):
        return User.objects.get(username=params['username'])


    @classmethod
    def resolve_resource_class(cls, model_class, related_descriptors={}):
        """
            Match the feature_class to an existing resource class by iterating through subclasses of self.__class__
            If no match occurs generate one if db_entity is specified, else None
        :param model_class:
        :param related_descriptors: Optionally provided a dictionary of related descriptors of the model_class to use to create related resource fields
        in the case of dynamic resource creation
        :return: The matching or created resource
        """
        resources = FootprintResource.match_existing_resources(model_class)
        if len(resources) > 1:
            logging.warn("Too many resources for model class: %s. Resources; %s" % (model_class, resources))
        resource = resources[0] if len(resources) > 0 else None
        return resource or \
            get_dynamic_resource_class(
                cls,
                model_class,
                fields=map_dict_to_dict(
                    lambda related_field_name, related_descriptor: cls.related_resource_field(related_field_name, related_descriptor),
                    related_descriptors))

    @classmethod
    def related_resource_field(cls, related_field_name, related_descriptor):
        """
           Returns a tuple of the related_field resource name and resource field. ManyToMany and ForeignKey is currently supported
        :param related_field_name: The related name on the model class
        :param related_descriptor: The related Field on the model class. Expected is an instance of models.ManyToMany, or models.ForeignKey
        :return: A tuple with the field.name or singularized version and the created resource field.
        All fields created have full=False and null=True with the assumption that the value is optional and a need not be nested
        """

        related_field = related_descriptor.field
        related_resource_class = FootprintResource.resolve_resource_class(related_field.rel.to)
        # Clear the related object field caches in case it didn't pick up the dynamic many-to-many field of cls's model
        clear_many_cache(related_field.rel.to)
        if isinstance(related_field, models.ManyToManyField):
            return [related_field.name, fields.ToManyField(related_resource_class, related_field.name, full=False, null=True)]
        if isinstance(related_field, models.ForeignKey):
            return [related_field.name, fields.ToOneField(related_resource_class, related_field.name, full=False, null=True)]

    @classmethod
    def match_existing_resources(cls, model_class):
        """
            Find all subclasses of self.__class__ whoses queryset model is the given model_class)
        :param model_class: The model class to match
        :return:
        """
        return match_subclasses(
            cls,
            lambda resource_class: not (hasattr(resource_class._meta, 'abstract') and resource_class._meta.abstract) and resource_class._meta.queryset and issubclass(model_class, resource_class._meta.queryset.model))
