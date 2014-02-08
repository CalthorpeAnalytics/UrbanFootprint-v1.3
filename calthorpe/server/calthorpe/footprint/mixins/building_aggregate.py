# This Python file uses the following encoding: utf-8

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
import itertools

__author__ = 'calthorpe'

from django.contrib.gis.db import models
from footprint.models.built_form.building_use_percent import BuildingUsePercent
from django.db.models import Sum
from collections import defaultdict


class BuildingAttributeAggregate(models.Model):
    """
    An abstract class that describes a high-level built form that has a
    :model:`built_forms.building_attributes.BuildingAttributeSet`, defines methods to aggregate attributes
    the classes :model:`built_forms.buildingtype.BuildingType` and :model:`built_forms.placetype.Placetype`
    according to the mix of their components.
    """
    class Meta:
        abstract = True
        app_label = 'footprint'

    def building_attributes_list(self):
        """
        Defines the basic required attributes of
        core attributes
        +++++++++++++++
        - floors
        - residential_average_lot_size
        - softscape_and_landscape_percent
        - pervious_hardscape_percent
        - impervious_hardscape_percent
        - total_far
        - impervious_roof_percent
        - parking_structure_square_feet
        - parking_spaces
        - irrigated_percent
        """

        return ['floors',
                'residential_average_lot_size',
                'softscape_and_landscape_percent',
                'pervious_hardscape_percent',
                'impervious_hardscape_percent',
                'total_far',
                'impervious_roof_percent',
                'parking_structure_square_feet',
                'parking_spaces',
                'irrigated_percent',
                ]

    def complete_aggregate_definition(self):
        """
        Checks that all the components have been established, to avoid redundant calculations
        :return: True or False
        """

        if self.get_all_components().aggregate(Sum('percent'))['percent__sum'] < .98:
            print 'components not all saved, skipping {0}'.format(self)
            return False
        else:
            return True

    def get_all_components(self):
        """
        Identifies the component class and returns the component_percent objects representing the relationship
        between the components and the BuildingAggregate
        :return: BuildingAggregate component_percents
        """
        component_percent_field = self.get_component_field().through.__name__
        component_percents = getattr(self, "{0}_set".format(component_percent_field.lower())).all()
        return component_percents

    def aggregate_built_form_attributes(self):
        """
        Grabs the component buildings of the BuildingAggregate and does a weighted average of their core attributes,
        before passing the building_attributes to the calculate_derived_fields() method.
        """
        if not self.complete_aggregate_definition():
            return

        self.building_attributes.gross_net_ratio = self.calculate_gross_net_ratio()

        for attribute in self.building_attributes_list():
            attribute_value = sum([
                (getattr(component_percent.component().building_attributes, attribute) or 0) *
                component_percent.percent for component_percent in self.get_all_components()
            ])

            setattr(self.building_attributes, attribute, attribute_value)

        self.building_attributes.save()
        self.aggregate_built_form_uses()
        self.building_attributes.calculate_derived_fields()
        self.save()

    def aggregate_built_form_uses(self):
        """
        Aggregates the attributes of the :model:`footprint.BuildingUsePercent` objects associated with the components
        of the aggregate built form, and creates new :model:`footprint.BuildingUsePercent` objects associated with the
        aggregate object.

        For each type of use (single family large lot, restaurant, etc) that is present in the components of the
        aggregate being assembled, a new BuildingUsePercent object is created and connected to the aggregate's
        BuildingAttributes. Attributes of the new BuildingUsePercent object are derived from the attributes of
        BuildingUsePercent objects in the components.

        Attributes are averaged with the method:
            Σ(attribute_value * component_use_percent * component_percent) / aggregate_use_percent

        where
            component_percent = the percent of the component within the aggregate
            component_use_percent = the percent of the use within the component
            aggregate_use_percent = the percent of the use within the aggregate

        for each use matching the current type of use in all of the components of the aggregate

        """
        from footprint.models import Placetype

        def get_component_percent(use_percent, component_percents):
            """
            gets the component_percent for the component_use_percent
            :param use_percent:
            :return:
            """
            building_attributes = use_percent.building_attributes
            components = [component_percent for component_percent in component_percents
                          if component_percent.component().building_attributes == building_attributes]
            return components[0].percent

        component_percents = self.get_all_components()

        component_use_percents = list(itertools.chain.from_iterable([
            list(component_percent.component().building_attributes.buildingusepercent_set.all())
            for component_percent in component_percents
        ]))

        component_use_definitions = set([
            component_use_percent.building_use_definition for component_use_percent in component_use_percents
        ])

        for use_definition in component_use_definitions:
            aggregate_use_attributes = defaultdict(lambda: 0.0000000000000000000000000)

            # makes a list of BuildingUsePercent objects of the use currently being aggregated
            use_percent_components = [component_use_percent for component_use_percent in component_use_percents
                                      if component_use_percent.building_use_definition.name == use_definition.name]

            aggregate_use_attributes['percent'] = sum([
                component_use_percent.percent *
                get_component_percent(component_use_percent, component_percents)
                for component_use_percent in use_percent_components
            ])

            attributes = use_definition.get_attributes()
           
            for attr in attributes:

                if attr in ['household_size', 'vacancy_rate', 'efficiency']:
                    aggregate_use_attributes[attr] = sum([

                        getattr(component_use_percent, attr) *
                        component_use_percent.percent *
                        get_component_percent(component_use_percent, component_percents)

                        for component_use_percent in use_percent_components

                    ]) / aggregate_use_attributes['percent']

                else:
                    aggregate_use_attributes[attr] = sum([
                        getattr(component_use_percent, attr) *
                        get_component_percent(component_use_percent, component_percents)
                        for component_use_percent in use_percent_components
                    ])


            BuildingUsePercent.objects.update_or_create(
                building_attributes=self.building_attributes,
                building_use_definition=use_definition,
                defaults=aggregate_use_attributes
            )