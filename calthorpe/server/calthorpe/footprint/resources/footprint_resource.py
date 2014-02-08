import logging
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from tastypie.authentication import ApiKeyAuthentication
from tastypie.exceptions import BadRequest
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.resources import csrf_exempt
from footprint.lib.functions import merge
import traceback

__author__ = 'calthorpe'

class FootprintResource(ModelResource):
    """
        Adds django revision with the tastypie ModelResource
    """
    def __init__(self):
        # Get an instance of a logger
        self.logger = logging.getLogger(__name__)
        super(ModelResource, self).__init__()

    class Meta(object):
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()

    # From http://django-tastypie.readthedocs.org/en/latest/cookbook.html
    def dispatch(self, request_type, request, **kwargs):
        self.logger.debug(
            '%s %s %s' %
            (request.method, request.get_full_path(), request.raw_post_data))

        try:
            response = super(ModelResource, self).dispatch(
                request_type, request, **kwargs)

            if request.method in ['POST', 'PATCH']:
                self.post_save(request, **kwargs)
        except (BadRequest, fields.ApiFieldError), e:
            self.logger.debug(
                'Response 400 %s' % e.args[0])
            raise
        except ValidationError, e:
            self.logger.debug(
                'Response 400 %s' % e.messages)
            raise
        except Exception, e:
            if hasattr(e, 'response'):
                self.logger.debug(
                    'Response %s %s %s' %
                    (e.response.status_code, e.response.content, traceback.format_exc()))
            else:
                self.logger.debug('Response 500')
            raise

        self.logger.debug(
            'Response %s %s' % (response.status_code, response.content))
        return response

    def wrap_view(self, view):
        """
            Overrides wrap_view to allow processing of dynamic resource classes. Special parameters such as config_entity_id are used to resolve the correct resource subclass.
        :param view:
        :return:
        """
        # TODO this csrf_exempt should be conditional and removed in production
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