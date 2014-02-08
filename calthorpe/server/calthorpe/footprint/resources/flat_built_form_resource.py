from footprint.models import FlatBuiltForm
from footprint.resources.footprint_resource import FootprintResource

__author__ = 'calthorpe'

class FlatBuiltFormResource(FootprintResource):

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = FlatBuiltForm.objects.all()
        resource_name = 'flat_built_form'
        filtering = {
            "built_form_id": ('exact',),
        }
