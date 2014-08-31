import logging
import traceback

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.http import HttpResponse
from tastypie.authentication import ApiKeyAuthentication
from tastypie.exceptions import BadRequest
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.models import ApiKey
from tastypie.http import HttpAccepted
from tastypie.models import ApiKey
from tastypie.resources import csrf_exempt
from tastypie.utils.mime import build_content_type

from footprint.main.lib.functions import map_dict_to_dict, merge
from footprint.main.models import DbEntity
from footprint.main.utils.dynamic_subclassing import get_dynamic_resource_class
from footprint.main.utils.subclasses import match_subclasses
from footprint.main.utils.utils import clear_many_cache, has_explicit_through_class, foreign_key_field_of_related_class
from tastypie.serializers import Serializer

__author__ = 'calthorpe_associates'


class FootprintSerializer(Serializer):
    def format_datetime(self, data):
        return data.strftime("%Y-%m-%dT%H:%M:%S")

class FootprintHttpAccepted(HttpAccepted):
    def __init__(self, content='', mimetype=None, status=None, content_type=None, objects=None):
        super(FootprintHttpAccepted, self).__init__(content, mimetype, status, content_type)
        self.objects = objects

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
        serializer = FootprintSerializer()

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
            if request.method in ['POST', 'PATCH']:
                self.pre_save(request, **kwargs)

            response = super(ModelResource, self).dispatch(
                request_type, request, **kwargs)

            if request.method in ['POST', 'PATCH']:
                self.post_save(request, response, **kwargs)

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


    def create_response(self, request, data, response_class=HttpResponse, **response_kwargs):
        """
        Extracts the common "which-format/serialize/return-response" cycle.

        Mostly a useful shortcut/hook.

        Overridden to include the original bundle, which is normally discard at this point
        """
        if response_class==HttpAccepted:
            response_class = FootprintHttpAccepted
        else:
            return super(FootprintResource, self).create_response(request, data, response_class, **response_kwargs)

        desired_format = self.determine_format(request)
        serialized = self.serialize(request, data, desired_format)
        objects = map(lambda bundle: bundle.obj, data.get('objects'))
        return response_class(content=serialized, content_type=build_content_type(desired_format),
                              **merge(response_kwargs,
                                      dict(objects=objects) if response_class == FootprintHttpAccepted else dict()))

    def save_m2m(self, bundle):
        """
            Overrides the super method in order to handle saving many-to-many collection instances of an explicit through class. For some reason tastypie has no handling for this, but we want to deliver the through class instances to the user that have references to the related attribute (e.g. DbEntityInterest instances are delivered and each has a reference to DbEntity). We also want to allow the client to modify, add, and remove these instances. Thus we must intercept them here and save them properly. Tastypie assumes non-explict Through classes and just dumbly tries to add them to the related field with add(), which fails for explicitly through classes.
        :param bundle:
        :return:
        """

        # This is an exact copy of the super method up until the add() line
        for field_name, field_object in self.fields.items():
            if not getattr(field_object, 'is_m2m', False):
                continue

            if not field_object.attribute:
                continue

            if field_object.readonly:
                continue

            # Get the manager.
            related_mngr = None

            if isinstance(field_object.attribute, basestring):
                related_mngr = getattr(bundle.obj, field_object.attribute)
            elif callable(field_object.attribute):
                related_mngr = field_object.attribute(bundle)

            if None==related_mngr:
                continue

                # This condition is an enhancement to the super method. It allows an add method defined on the field to indicate how to add the many-to-many items
                # We don't use this since our items are handled more carefully below
                #if hasattr(related_mngr, 'clear'):
                # Clear it out, just to be safe.
            #    related_mngr.clear()

            existing_related_objs = related_mngr.all()
            related_objs_to_add = []

            # TODO handle remove and clear
            if hasattr(field_object, 'add'):
                # This condition is an enhancement to the super method.
                # It allows an add method defined on the field to indicate how to add the many-to-many items
                related_objs_to_add = map(lambda bundle: bundle.obj, bundle.data[field_name])
                # Call the custom defined add
                field_object.add(bundle, *related_objs_to_add)
                related_objs_to_remove = list(set(existing_related_objs)-set(related_objs_to_add))
                # Optionally call remove. The add function might take care of removing existing instances instead
                if hasattr(field_object, 'remove') and hasattr(field_object.remove, '__call__'):
                    field_object.remove(bundle, *related_objs_to_remove)
            else:
                explicit_through_class = has_explicit_through_class(bundle.obj, field_object.instance_name)
                if explicit_through_class:
                    to_model_attr = foreign_key_field_of_related_class(related_bundle.obj.__class__, bundle.obj.__class__).name,
                existing_related_objs = related_mngr.all()
                for related_bundle in bundle.data[field_name]:
                    # This if statement is a change from the super method. If we are handling explict through instances we need to give the incoming instance a reference to the bundle.obj. The through instances are never dehydrated with this reference since it simply refers back to the container (bundle.data)
                    if explicit_through_class:
                        # Set one side of the relationship to bundle.obj. This might have already been done on the client, but this overrides
                        setattr(
                            related_bundle.obj,
                            # Figure out the correct field
                            to_model_attr,
                            bundle.obj)
                    # Save the instance no matter what
                    related_bundle.obj.save()
                    # Create a list of objects to add to the manager
                    related_objs_to_add.append(related_bundle.obj)
                # Create the set of objects to remove (ones that existed but weren't in the incoming related_bundle)
                related_objs_to_remove = list(set(existing_related_objs)-set(related_objs_to_add))
                # If we are handling explict through instances the save above is adequate. We don't want to try to add the item to the manager.
                # These methods are thus only for implicit related fields (no explicit through class)
                if hasattr(related_mngr, 'add'):
                    related_mngr.add(*related_objs_to_add)
                if hasattr(related_mngr, 'remove'):
                    related_mngr.remove(*related_objs_to_remove)

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

    def pre_save(self, request, **kwargs):
        """
            Presave operations to perform for the model class after
            POST, PUT, and PATCH. We don't have access to the objects
            like on post_save, so this is only useful to turn off
            class-scope publishing and similar
        """
        params = request.GET
        user_id = ApiKey.objects.get(key=params['api_key']).user_id
        model_class = self._meta.queryset.model
        if hasattr(model_class, 'pre_save'):
            model_class.pre_save(user_id, **kwargs)

    def post_save(self, request, response, **kwargs):
        """
            Optional operations to perform after POST, PUT, and PATCH
        :param request:
        :return:
        """
        objects = response.objects if hasattr(response, 'objects') else None
        params = request.GET
        user_id = ApiKey.objects.get(key=params['api_key']).user_id
        model_class = self._meta.queryset.model
        if hasattr(model_class, 'post_save'):
            model_class.post_save(user_id, objects, **kwargs)

    def resolve_user(self, params):
        return User.objects.get(username=params['username'])


    @classmethod
    def resolve_resource_class(cls, model_class, related_descriptors={}, queryset=None, base_resource_class=None, object_class=None):
        """
            Match the feature_class to an existing resource class by iterating through subclasses of self.__class__
            If no match occurs generate one if db_entity is specified, else None
        :param model_class:
        :param related_descriptors: Optionally provided a dictionary of related descriptors of the model_class to use to create related resource fields
        in the case of dynamic resource creation
        :return: The matching or created resource
        """
        logger = logging.getLogger(__name__)

        if not base_resource_class and not queryset:
            resources = FootprintResource.match_existing_resources(model_class)
            if len(resources) > 1:
                logging.warn("Too many resources for model class: %s. Resources; %s" % (model_class, resources))
            resource = resources[0] if len(resources) > 0 else None
            logger.debug("Found existing resource class %s for model class %s" % (resource, model_class))
        else:
            resource = None
            logger.debug("No existing resource class for model class %s" % (model_class))
            logger = None

        limit_api_fields = hasattr(model_class, 'limited_api_fields') and model_class.limited_api_fields()
        return resource or \
            get_dynamic_resource_class(
                base_resource_class or cls,
                model_class,
                # Created related fields from the related_descriptors
                fields=map_dict_to_dict(
                    lambda related_field_name, related_descriptor: cls.related_resource_field(related_field_name, related_descriptor),
                    related_descriptors),
                # Optionally set the fields and queryset on the Meta class
                meta_fields=merge(
                    dict(fields=limit_api_fields) if limit_api_fields else dict(),
                    dict(queryset=queryset, object_class=object_class) if queryset else dict()
                )
            )

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
            lambda resource_class: not (hasattr(resource_class._meta, 'abstract') and \
                                        resource_class._meta.abstract) and \
                                   resource_class._meta.queryset and \
                                   issubclass(model_class, resource_class._meta.queryset.model))
