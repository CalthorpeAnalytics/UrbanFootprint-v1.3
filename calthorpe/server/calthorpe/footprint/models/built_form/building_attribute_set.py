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
from decimal import Decimal
from django.db.models import Sum
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.models.constants import Constants
from footprint.models.built_form.building_use_percent import BuildingUsePercent
from footprint.utils.utils import get_or_none_from_queryset

__author__ = 'calthorpe'
from collections import defaultdict
from django.contrib.gis.db import models
from footprint.models.built_form.building_use_definition import BuildingUseDefinition
from footprint.models.keys.keys import Keys


class BuildingAttributeSet(models.Model):
    """
    Attributes of a :models:`footprint.Building`, :models:`footprint.BuildingType`, or :models:`footprint.Placetype`,
    including a reference to its uses through :model:`built_form.building_use_percent.BuildingUsePercent`.
    """
    objects = GeoInheritanceManager()

    class Meta(object):
        abstract = False
        app_label = 'footprint'

    def attributes(self):
        return "building"

    ## fields applicable at the Building level and above :
    building_uses = models.ManyToManyField(BuildingUseDefinition, through="BuildingUsePercent")

    parking_spaces = models.DecimalField(max_digits=7, decimal_places=3, default=0)
    parking_structure_square_feet = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    floors = models.DecimalField(max_digits=7, decimal_places=3, null=True)
    total_far = models.DecimalField(max_digits=10, decimal_places=7, null=True)

    # population fields
    gross_population_density = models.DecimalField(max_digits=14, decimal_places=10, default=0)
    household_density = models.DecimalField(max_digits=14, decimal_places=10, default=0)

    # these should really be optional / derived ...
    impervious_roof_percent = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    impervious_hardscape_percent = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    pervious_hardscape_percent = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    softscape_and_landscape_percent = models.DecimalField(max_digits=5, decimal_places=3, null=True)

    irrigated_percent = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    hardscape_percent = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    residential_irrigated_square_feet = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    commercial_irrigated_square_feet = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    residential_average_lot_size = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    gross_net_ratio = models.DecimalField(max_digits=8, decimal_places=7, default=1)

    combined_pop_emp_density = models.DecimalField(max_digits=9, decimal_places=4, default=0)

    # methods to get at derived facts about building attributes
    def calculate_combined_pop_emp_density(self):
        employment_uses = self.buildingusepercent_set.filter(
            building_use_definition__name__in=Keys.TOP_LEVEL_EMPLOYMENT_CATEGORIES)

        emp_density = self.get_unit_density(employment_uses) if employment_uses.exists else 0
        self.combined_pop_emp_density = float(emp_density) + float(self.gross_population_density or 0)

    def calculate_derived_fields(self):
        """
        takes the basic input data about the building attributes of a built form, and calculates useful derived fields
        for use by the flat_built_forms exporter and eventually in integrated UF analyses
        :return:
        """
        from footprint.models.built_form.primary_component import PrimaryComponent

        for use_percent in self.buildingusepercent_set.all():
            if isinstance(self.builtform_set.select_subclasses()[0], PrimaryComponent):
                use_percent.calculate_derived_attributes()

        self.calculate_use_metacategories()

        self.calculate_residential_attributes()

        # derive irrigated square feet fields
        self.hardscape_percent = (self.impervious_roof_percent or 0) + (self.impervious_hardscape_percent or 0)

        if self.floors and not self.hardscape_percent:
            building_footprint = self.total_far / self.floors
            parking_space_area = self.parking_spaces * Constants.PARKING_STALL_SQUARE_FEET
            uncovered_parking_area = parking_space_area - self.parking_structure_square_feet
            self.hardscape_percent = (building_footprint + uncovered_parking_area) / Constants.SQUARE_FEET_PER_ACRE

        commercial_uses = self.buildingusepercent_set.filter(
            building_use_definition__name__in=['Retail', 'Office', 'Industrial']
        )
        residential_uses = self.buildingusepercent_set.filter(
            building_use_definition__name__in=Keys.RESIDENTIAL_SUBCATEGORIES
        )

        percent_residential = residential_uses.aggregate(Sum('percent'))['percent__sum'] or 0
        percent_commercial = commercial_uses.aggregate(Sum('percent'))['percent__sum'] or 0

        available_irrigation_area = (self.softscape_and_landscape_percent or 0) * Constants.SQUARE_FEET_PER_ACRE
        irrigated_area = available_irrigation_area * (self.irrigated_percent or 0)

        self.residential_irrigated_square_feet = float(percent_residential) * float(irrigated_area or 0)
        self.commercial_irrigated_square_feet = float(percent_commercial) * float(irrigated_area or 0)
        self.calculate_combined_pop_emp_density()
        self.save()

    def get_unit_density(self, use_percent_set):
        return sum(building_use.unit_density for building_use in use_percent_set)

    def calculate_use_metacategories(self):
        """
        Calculates upper level uses for the built form based on the attributes
        :return:
        """
        metacategories = ["RESIDENTIAL", "OFFICE", "RETAIL", "INDUSTRIAL", "AGRICULTURAL"]

        for metacategory in metacategories:

            metacategory_name = getattr(Keys, "{0}_CATEGORY".format(metacategory))
            metacategory_definition = BuildingUseDefinition.objects.get_or_create(name=metacategory_name)[0]
            subcategory_names = getattr(Keys, "{0}_SUBCATEGORIES".format(metacategory))

            subcategories = self.buildingusepercent_set.filter(building_use_definition__name__in=subcategory_names)

            metacategory_dict = defaultdict(lambda: Decimal(0.000000000000))

            metacategory_dict['percent'] = subcategories.aggregate(Sum('percent'))['percent__sum']
            if not metacategory_dict['percent']:
                continue

            averaged_attributes = metacategory_definition.averaged_attributes()
            summed_attributes = metacategory_definition.summed_attributes()

            for attribute in averaged_attributes:
                metacategory_dict[attribute] = sum([
                    getattr(subcategory, attribute) * (subcategory.percent / metacategory_dict['percent'])
                    for subcategory in subcategories
                ])
            for attribute in summed_attributes:
                metacategory_dict[attribute] = sum([getattr(subcategory, attribute) for subcategory in subcategories])

            
            BuildingUsePercent.objects.update_or_create(
                building_attributes=self,
                building_use_definition=BuildingUseDefinition.objects.get(name=metacategory_name),
                defaults=metacategory_dict
            )

        return BuildingUsePercent.objects.filter(
            building_use_definition__name__in=Keys.BUILDING_USE_DEFINITION_METACATEGORIES
        )

    def calculate_residential_attributes(self):
        """
        does special calculations for residential attributes, or just returns if there isn't any residential use:

        household_density = [unit_density] * (1 - vacancy_rate)

        gross_population_density = [household_density] * [household_size]

        :return:
        """

        use = get_or_none_from_queryset(
            self.buildingusepercent_set,
            building_use_definition__name=Keys.RESIDENTIAL_CATEGORY
        )

        if not use:
            return

        self.household_density = use.unit_density * (1-use.vacancy_rate)
        self.gross_population_density = self.household_density * use.household_size
        self.save()