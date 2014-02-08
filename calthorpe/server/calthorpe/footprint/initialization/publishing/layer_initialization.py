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
from footprint.initialization.fixture import LayerConfigurationFixture, project_schemas_of_client
from footprint.initialization.utils import resolve_fixture
from footprint.models.tag import Tag
from footprint.models.keys.keys import Keys
from footprint.models.signals import initialize_media
from footprint.utils.utils import create_media_subdir
import settings

__author__ = 'calthorpe'

@receiver(initialize_media)
def initialize_media(sender, **kwargs):
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
    # Create a PresentationConfiguration for each layer library. This serves to set what layers are initially visible and what db_entities are made into layers

    Tag.objects.update_or_create(tag=LayerTag.BACKGROUND)
    Tag.objects.update_or_create(tag=LayerTag.DEFAULT)
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
    BACKGROUND = 'background'
    DEFAULT = 'default'

class LayerSort(object):
    FUTURE = 10
    BASE = 20
    OTHER = 60
    BACKGROUND = 80
