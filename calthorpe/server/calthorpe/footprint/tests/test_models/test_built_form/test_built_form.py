from footprint.models.built_form.building_attribute_set import BuildingAttributeSet

__author__ = 'calthorpe'
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
from footprint.utils.test_utils import reasonably_close
import unittest
from itertools import chain
from django.db.models import Sum
from footprint.models.built_form.flat_built_forms import refresh_all_flat_built_forms
from footprint.models.keys.keys import Keys

from footprint.models.config.global_config import global_config_singleton
from footprint.models.application_initialization import application_initialization

from footprint.models.built_form.placetype import Placetype
from footprint.models.built_form.buildingtype import BuildingType
from footprint.models.built_form.building import Building
from footprint.models.built_form.infrastructure_type import InfrastructureType

from footprint.tests.test_data import sample_built_form_sets

from footprint.initialization.data_provider import DataProvider

class TestBuiltForm(unittest.TestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_import_from_fixtures(self):
        DataProvider().built_form_sets()
        print "OKAY"

    def test_building_imports(self):
        def sum_import_building_subcategories(building):
            return sum(
                [building.percent_single_family_large_lot, building.percent_single_family_small_lot,
                 building.percent_attached_single_family, building.percent_multifamily_2_to_4,
                 building.percent_multifamily_5_plus,

                 # Pct_Emp_Office_Svc,Pct_Educ_Svc,Pct_Medical_Svc,Pct_Public_Admin,
                 building.percent_office_services, building.percent_education_services,
                 building.percent_medical_services, building.percent_public_admin,

                 #Pct_Retail_Svc,Pct_Restuarant,Pct_Accommodation,Pct_Arts_Entertainment,Pct_Other_Svc,
                 building.percent_retail_services, building.percent_restaurant, building.percent_accommodation,
                 building.percent_arts_entertainment, building.percent_other_services,

                 # Pct_Manufacturing,Pct_Transport_warehouse,Pct_Wholesale,Pct_Construction_Util,Pct_Agriculture,
                 # Pct_Extraction,
                 building.percent_manufacturing, building.percent_transport_warehouse, building.percent_wholesale,
                 building.percent_construction_utilities, building.percent_agriculture, building.percent_extraction]
            )

        def sum_building_industrial_uses(building):
            return sum([building.percent_manufacturing, building.percent_transport_warehouse, building.percent_wholesale,
                 building.percent_construction_utilities, building.percent_agriculture, building.percent_extraction])

        def sum_building_retail_uses(building):
            return sum([building.percent_retail_services, building.percent_restaurant, building.percent_accommodation,
                 building.percent_arts_entertainment, building.percent_other_services])

        def sum_import_building_categories(building):
            return sum(
                [building.percent_industrial, building.percent_retail, building.percent_office,
                 building.percent_residential]
            )

        def sum_building_residential_uses(building):
            return sum(
                [building.percent_single_family_large_lot, building.percent_single_family_small_lot,
                 building.percent_attached_single_family, building.percent_multifamily_2_to_4,
                 building.percent_multifamily_5_plus]
            )

        def sum_building_office_uses(building):
            return sum(
                [building.percent_office_services, building.percent_education_services,
                 building.percent_medical_services, building.percent_public_admin])

        for building in sample_built_form_sets.load_buildings_csv():
            assert reasonably_close(sum_building_office_uses(building), building.percent_office)
            assert reasonably_close(sum_building_residential_uses(building), building.percent_residential)
            assert reasonably_close(sum_building_retail_uses(building), building.percent_retail)
            assert reasonably_close(sum_building_industrial_uses(building), building.percent_industrial)

            assert building.percent_of_building_type >= 0,"{0} has a percent less than zero !".format(building)
            assert .95 < sum_import_building_subcategories(building) < 1.05, \
                "{0}, {1}".format(building.name,sum_import_building_subcategories(building))
            assert .95 < sum_import_building_categories(building) < 1.05, \
                "{0}, {1}".format(building.name,sum_import_building_categories(building))

            if sum_building_office_uses(building) > 0:
                assert building.office_efficiency > 0,  "{0}, {1}".format(building.name,building.office_efficiency)
                assert building.office_square_feet_per_unit > 0, "{0}, {1}".format(building.name.building.office_square_feet_per_unit)

            if sum_building_residential_uses(building) > 0:
                assert building.residential_square_feet_per_unit > 0,  "{0}, {1}".format(building.name.building.square_feet_per_unit)
                assert building.residential_efficiency > 0,  "{0}, {1}".format(building.name.building.residential_efficiency)
            if sum([building.percent_single_family_large_lot, building.percent_single_family_small_lot]) > 0:
                assert building.residential_average_lot_size > 0, "{0}, {1}".format(building.name.building.residential_average_lot_size)
        return True

    def test_built_form_exports(self):
        refresh_all_flat_built_forms()
        
    def test_unit_density(self):
        application_initialization()
        for built_form in BuildingAttributeSet.objects.all():
            built_form.calculate_combined_pop_emp_density()
            built_form.save()

    def test_built_form(self):
        application_initialization()

        assert self.test_building_imports() is True

        global_config = global_config_singleton()
        built_form_set = global_config.built_form_sets.all()

        test_buildings = Building.objects.all()
        test_buildingtypes = BuildingType.objects.all()
        test_placetypes = Placetype.objects.all()
        test_infrastructuretypes = InfrastructureType.objects.all()

        assert test_buildings.exists() is True
        assert test_buildingtypes.exists() is True
        assert test_placetypes.exists() is True
        assert test_infrastructuretypes.exists() is True

        for built_form in chain(test_buildings, test_buildingtypes, test_placetypes):
            # built_form.aggregate_built_form_attributes()
            # built_form.building_attributes.calculate_derived_fields()
            for use in built_form.building_attributes.buildingusepercent_set.all():
                assert use.efficiency > 0, "{0} {1}".format(built_form, use.building_use_definition.name)
                assert use.percent > 0, "{0} {1}".format(built_form, use.building_use_definition.name)

        # all built forms that are aggregates of other built forms must have components that add to 100%
        for aggregate_built_form in chain(test_buildingtypes, test_placetypes):
            component_percent_field = aggregate_built_form.get_component_field().through.__name__
            component_percents = getattr(aggregate_built_form, "{0}_set".format(component_percent_field.lower())).all()
            components_percents_sum = component_percents.aggregate(Sum('percent'))['percent__sum']

            assert .95 < components_percents_sum < 1.05, \
                'BAD THING: components of {0} add up to {1} %'.format(aggregate_built_form.name, components_percents_sum*100)
            if components_percents_sum != 1:
                print aggregate_built_form.name, 'component_error ', components_percents_sum*100

        assert Building.objects.filter(building_attributes__parking_spaces__gt=0).exists() == True
        assert BuildingType.objects.filter(building_attributes__parking_spaces__gt=0).exists() == True
        assert Placetype.objects.filter(building_attributes__parking_spaces__gt=0).exists() == True

        assert Building.objects.filter(building_attributes__impervious_hardscape_percent__gt=0).exists() == True
        assert BuildingType.objects.filter(building_attributes__impervious_hardscape_percent__gt=0).exists() == True
        assert Placetype.objects.filter(building_attributes__impervious_hardscape_percent__gt=0).exists() == True

        assert Building.objects.filter(building_attributes__impervious_roof_percent__gt=0).exists() == True
        assert BuildingType.objects.filter(building_attributes__impervious_roof_percent__gt=0).exists() == True
        assert Placetype.objects.filter(building_attributes__impervious_roof_percent__gt=0).exists() == True

        # all built forms based on buildings must have building uses that sum to 100%
        for built_form in chain(test_buildings, test_buildingtypes, test_placetypes):
            for use in built_form.building_attributes.buildingusepercent_set.all():
                assert use.efficiency > 0, "{0} {1}".format(built_form, use.building_use_definition.name)

            assert 1 >= built_form.building_attributes.gross_net_ratio > 0, \
                '{0} has ratio of {1}'.format(built_form.name, built_form.building_attributes.gross_net_ratio)

            assert built_form.building_attributes.total_far > 0, '{0} has floor area ratio of {1}'.format(built_form.name, built_form.building_attributes.total_far)

            building_uses = built_form.building_attributes.buildingusepercent_set.all()
            assert building_uses.exists(), built_form

            building_use_categories = building_uses.filter(
                building_use_definition__name__in=[
                    Keys.RESIDENTIAL_CATEGORY,
                    Keys.RETAIL_CATEGORY,
                    Keys.OFFICE_CATEGORY,
                    Keys.INDUSTRIAL_CATEGORY,
                    Keys.AGRICULTURAL_CATEGORY,
                    Keys.MILITARY_CATEGORY]
            )

            building_use_subcategories = building_uses.exclude(id__in=building_use_categories.values_list('id', flat=True))

            for building_use_categories in [building_use_subcategories, building_use_categories]:
                if building_use_categories == building_use_subcategories:
                    category_type = 'subcategory'
                else:
                    category_type = 'high level category'

                described_uses = building_use_categories.aggregate(Sum('percent'))['percent__sum']
                assert described_uses > 0, '{0} {1} ({2})'.format(built_form.__class__.__name__, built_form.name, category_type)

                described_use_coverage = described_uses / built_form.building_attributes.gross_net_ratio
                assert .5 < described_use_coverage < 1.5, 'Built form {0} has uses describing {1} percent (should be 100)'\
                                                                .format(built_form.name, described_use_coverage*100)
                if described_use_coverage != 1:
                    print 'BAD THING: uses of {0} {1} add up to {2} % \n  gross/net ratio = {3} \t use = {4} \n \
                    '.format(built_form.__class__.__name__, built_form.name, described_use_coverage*100,
                        built_form.building_attributes.gross_net_ratio, described_uses )

                assert .97  < described_use_coverage < 1.03, \
                    'BAD THING: uses of {0} add up to {1} % \n  gross/net ratio = {2} \n use = {3} \n \
                    '.format(built_form.name, described_use_coverage*100,
                        built_form.building_attributes.gross_net_ratio, described_uses)

            for building_use in building_uses:
                assert 1 >= building_use.efficiency > 0, '{0} {1} has efficiency of {2} for {3}'.format(
                    built_form.__class__.__name__, built_form.name, building_use.efficiency, building_use.building_use_definition.name)

                assert building_use.square_feet_per_unit > 0, '{0} for {1} has {2} square feet per unit'.format(
                    building_use.building_use_definition.name, built_form.name , building_use.efficiency)

            # with the input fields correctly aggregated, we can now begin deriving the secondary fields

            for use in built_form.building_attributes.buildingusepercent_set.all():
                assert use.unit_density > 0, '{0} {1} has unit density of {2} for {3}'.format(
                    built_form.__class__.__name__, built_form.name, use.unit_density, use.building_use_definition.name)
                assert use.floor_area_ratio > 0, '{0} {1} has far of {2} for {3}'.format(
                    built_form.__class__.__name__, built_form.name, use.floor_area_ratio, use.building_use_definition.name)
                assert use.gross_built_up_area > 0, '{0} {1} has gross built up area of {2} for {3}'.format(
                    built_form.__class__.__name__, built_form.name, use.gross_built_up_area, use.building_use_definition.name)
                assert use.net_built_up_area > 0, '{0} {1} has net built up area of {2} for {3}'.format(
                    built_form.__class__.__name__, built_form.name, use.net_built_up_area, use.building_use_definition.name)

