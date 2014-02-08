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
from django.dispatch import receiver
from footprint.client.configuration.fixture import LayerConfigurationFixture
from footprint.client.configuration.utils import resolve_fixture
from footprint.main.models.tag import Tag
from footprint.main.models.keys.keys import Keys
from footprint.main.models.signals import initialize_media
from footprint.main.utils.utils import create_media_subdir
from footprint import settings

__author__ = 'calthorpe_associates'

@receiver(initialize_media)
def initialize_layer_media(sender, **kwargs):
    """
        This fires when the application initializes or updates. It creates all the media need by tilestache, namely
        style templates and their default contexts
    :param sender:
    :param kwargs
    :return:
    """

    # TODO can we write media to the DB without/instead of the filesystem??
    create_media_subdir('styles')
    create_media_subdir('cartocss')

    Tag.objects.update_or_create(tag=LayerTag.BACKGROUND_IMAGERY)
    Tag.objects.update_or_create(tag=LayerTag.DEFAULT)

    layer_fixture = resolve_fixture(
        "publishing",
        "layer",
        LayerConfigurationFixture,
        settings.CLIENT)
    layer_fixture.update_or_create_media()



class LayerLibraryKey(Keys):
    class Fab(Keys.Fab):
        @classmethod
        def prefix(cls):
            return 'layer_library'

    # The default layer library
    DEFAULT = Fab.ricate('default')

class LayerKey(Keys):
    class Fab(Keys.Fab):
        @classmethod
        def prefix(cls):
            return 'layer'

class LayerMediumKey(LayerKey):
    class Fab(Keys.Fab):
        @classmethod
        def prefix(cls):
            return 'layer_medium'

    # The default medium for all layers
    DEFAULT = Fab.ricate('default')

class LayerTag(Keys):
    BACKGROUND_IMAGERY = 'background_imagery'
    DEFAULT = 'urbanfootprint_layers'

class LayerSort(object):
    FUTURE = 10
    BASE = 20
    OTHER = 60
    BACKGROUND = 80
