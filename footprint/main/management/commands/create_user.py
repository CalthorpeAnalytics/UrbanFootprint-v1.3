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
from optparse import make_option
import logging
from django.contrib.auth.models import User, Permission
from django.core.management.base import BaseCommand
from tastypie.models import ApiKey
from footprint.main.lib.functions import get_single_value_or_create
from footprint.main.management.commands.footprint_init import all_config_entities
from footprint.main.publishing import tilestache_publishing

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
        This command clears all layer_selections
    """
    option_list = BaseCommand.option_list + (
        make_option('--username', default='', help='The username'),
        make_option('--password', default='', help='The password'),
        make_option('--email', default='', help='The email'),
    )

    def handle(self, *args, **options):
        if options['username'] and options['password'] and options['email']:
            self.user(options['username'], options['password'], options['email'])
            for config_entity in all_config_entities():
                tilestache_publishing.on_config_entity_post_save_tilestache(None, instance=config_entity)
        else:
            raise Exception("Required: --username, --password, and --email")

    def user(self, username, password, email, api_key=None):
        """
        Create a user.
        :return:
        """

        def create():
            user = User.objects.create_user(username, email, password)
            # Make sure the user has permission to update everything for testing purposes
            user.user_permissions.add(*list(Permission.objects.all()))
            return user
            # An api key is created upon creating a user

        user = get_single_value_or_create(User.objects.filter(username=username), create)
        api_key_instance = ApiKey.objects.get_or_create(user=user)[0]
        if api_key_instance.key != api_key:
            api_key_instance.key = api_key
            api_key_instance.save()
        return {'user': user, 'api_key': api_key_instance}

