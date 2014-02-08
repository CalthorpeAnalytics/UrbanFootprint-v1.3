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
from django.template import Context
from django.template.loader import get_template_from_string
from picklefield.fields import PickledObjectField
from footprint.lib.functions import map_dict_to_dict, merge
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.models.presentation.medium import Medium

__author__ = 'calthorpe'


class Template(Medium):
    """
        Represents a Django-style template that needs additional data to be a usable Medium. It thus references a
        TemplateContext which might be XML, JSON, etc that has been parsed to python and can be used to populate the
        template. The Django style template string with wildcards (handlebars) must be stored in the content property.
        The template.template_context contains the default python dictionary to use to fill in the handlebars ({{ }})
        in the template.
    """
    objects = GeoInheritanceManager()

    template_context = PickledObjectField()

    def render_attributed_content(self, medium_context, content_key=None):
        """
            Given the medium_context for a PresentationMedium, render the default template with the medium_context values
        :param medium_context:
        :param content_key:
        :return:
        """

        rendered_attribute_content = map_dict_to_dict(
        # For each attribute key get the template dict if one exists and resolve the dict value for the given content_key
        # If no content_key exists just take the entire dict
            lambda key, value:
                [key,
                 get_template_from_string(
                     value.get(content_key, value).replace('\n', '').replace('   ', '')).render(Context(medium_context['attributes'][key]))
                ],
            self.content['attributes']) if 'attributes' in medium_context else None
        # Return a new dict based on the original medium_context with the attributes key/value overridden
        return merge(medium_context, dict(attributes=rendered_attribute_content))

    def render_content(self, medium_context, content_key=None):
        """
            Given the medium_context for a PresentationMedium, render the default template with the medium_context values
        :param medium_context:
        :param content_key:
        :return:
        """
        return get_template_from_string(
            self.content.get(content_key, self.content).replace('\n', '').replace('   ', '').render(Context(medium_context))) if medium_context else None

    class Meta(object):
        app_label = 'footprint'

