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
import os
from django import forms
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from tastypie.models import ApiKey
from footprint import settings


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

@csrf_exempt
def upload(request):
    if request.method != 'POST':
        form = UploadFileForm()
        return render_to_response('footprint/upload.html', {'form': form, 'api_key':ApiKey.objects.all()[0].key})

    api_key = request.GET.get('api_key', request.POST.get('api_key', None))
    user = User.objects.get(id=ApiKey.objects.get(key=api_key).user_id)
    progress_id = request.GET.get('X-Progress-ID', 'FORM_TEST')
    upload_id = '%s__%s' % (user.username, progress_id)
    f = request.FILES.get('files[]', None)
    # We need the extension so we know what file type to load
    extension = os.path.splitext(f.name)[-1]
    path = '%s%s%s' % (settings.TEMP_DIR, upload_id, extension)
    if not f:
        return HttpResponse()
    destination = open(path, 'wb+')

    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    os.chmod(path, 0777)
    # return status to client
    return HttpResponse(simplejson.dumps(dict(upload_id=upload_id)))

def get_upload_progress(request):
    cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], request.GET['X-Progress-ID'])
    data = cache.get(cache_key)
    return HttpResponse(simplejson.dumps(data))

