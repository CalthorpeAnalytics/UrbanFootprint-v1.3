# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
from tastypie.fields import DictField
from footprint.main.resources.presentation_medium_resource import PresentationMediumResource
from footprint.main.resources.presentation_resources import PresentationResource
from footprint.main.models import ResultLibrary, Result
from footprint.main.resources.mixins.mixins import ToManyFieldWithSubclasses

class ResultLibraryResource(PresentationResource):

    results = ToManyFieldWithSubclasses(
        'footprint.main.resources.result_resources.ResultResource',
        attribute='results',
        full=False,
        null=True)

    class Meta(PresentationResource.Meta):
        resource_name = 'result_library'
        always_return_data = True
        queryset = ResultLibrary.objects.all()
        excludes = ['presentation_media']

class ResultResource(PresentationMediumResource):

    # Returns the results of the DbEntity query
    query = DictField(attribute='query', null=False)

    class Meta(PresentationMediumResource.Meta):
        resource_name = 'result'
        always_return_data = True
        queryset = Result.objects.all()

