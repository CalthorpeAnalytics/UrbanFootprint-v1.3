

# coding=utf-8
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
import logging
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.built_form.agriculture.agriculture_attribute_set import AgricultureAttributeSet
from footprint.main.models.built_form.placetype import Placetype
from footprint.main.models.built_form.built_form import BuiltForm

__author__ = 'calthorpe_associates'
logger = logging.getLogger(__name__)

# noinspection PySingleQuotedDocstring
class LandscapeType(Placetype, AgricultureAttributeSet):
    """
    Placetypes are a set of BuildingTypes with a percent mix applied to each BuildingType
    """
    objects = GeoInheritanceManager()

    # So the model is pluralized correctly in the admin.
    class Meta(BuiltForm.Meta):
        verbose_name_plural = "Landscape Types"
        app_label = 'main'