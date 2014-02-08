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

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
import simplejson
from footprint.models import Placetype
from footprint.resources.resource_utils import unbundle
from footprint.resources.user_resource import UserResource

import  sys
sys.path.append(settings.CALTHORPE_ENGINE_PATH)

# TODO this bypasses the Tastypie API until I can figure out how to call the API without an ApiKey
def api_authentication(request):
    """
        Returns the current User instance via Tastypie, or accepts a username and password
    :param request:
    :return:
    """
    username = request.GET.get('username', None)
    password = request.GET.get('password', None)
    if username and password:
        user = authenticate(username=username, password=password)
    else:
        user = request.user

    resource_instance = UserResource()
    dehydrated = unbundle(resource_instance.full_dehydrate(resource_instance.build_bundle(obj=user)))
    data = simplejson.dumps(dehydrated, ensure_ascii='false')
    return HttpResponse(data,  mimetype="application/json")

def common_context(request):
    """
    The context items used by all pages. This dictionary is merged with that of the view method
    """

    user = request.user
    # Add permissions if needed
    #user.user_permissions.add(*list(Permission.objects.all()))

    return {
        'api_key':ApiKey.objects.get(user=user).key if user else '',
        'username':user.username if user else '',
        }

def scenario_context(request, scenario_id):

    s = Scenario.objects.filter(id=scenario_id)
    if len(s)==0:
        raise Exception("Scenario with id {0} does not exist".format(scenario_id))
    scenario = s[0]
    scenario_context = merge(common_context(request), {
        's' : scenario,
        'scenario_id' : scenario_id,
        })
    return scenario_context


def sandbox_data(request):
    placetypes = Placetype.objects.all()
    return render(request, 'footprint/chart_sandbox.html', {'placetypes': placetypes})