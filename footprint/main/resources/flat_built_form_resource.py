from footprint.main.models import FlatBuiltForm
from footprint.main.resources.footprint_resource import FootprintResource

__author__ = 'calthorpe_associates'

class FlatBuiltFormResource(FootprintResource):

    class Meta(FootprintResource.Meta):
        always_return_data = True
        queryset = FlatBuiltForm.objects.all()
        resource_name = 'flat_built_form'
        filtering = {
            "built_form_id": ('exact',),
        }
