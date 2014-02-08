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
from csvImporter.fields import CharField, FloatField, IntegerField
from csvImporter.model import CsvModel

__author__ = 'calthorpe'

class ImportPrimaryComponent(CsvModel):
    # id
    id = IntegerField(prepare=lambda x: x or 0)
    #source,hyperlink,building_type,
    source = CharField(prepare=lambda x: x or '')
    hyperlink = CharField(prepare=lambda x: x or '')
    placetype_component = CharField(prepare=lambda x: x or '')
    #building,household_size,
    name = CharField(prepare=lambda x: x or '')

    vacancy_rate = FloatField(prepare=lambda x: x or 0)
    household_size = FloatField(prepare=lambda x: x or 0)

    #all_uses,
    all_uses = CharField(prepare=lambda x: x or '')

    du_density = CharField(prepare=lambda x: x or '')
    emp_density = CharField(prepare=lambda x: x or '')

#Pct_SF_Large_Lot,Pct_SF_Small_Lot,Pct_Attached_SF,Pct_MF_2_to_4,Pct_MF_5_Plus,
    percent_single_family_large_lot = FloatField(prepare=lambda x: x or 0)
    percent_single_family_small_lot = FloatField(prepare=lambda x: x or 0)
    percent_attached_single_family = FloatField(prepare=lambda x: x or 0)
    percent_multifamily_2_to_4 = FloatField(prepare=lambda x: x or 0)
    percent_multifamily_5_plus = FloatField(prepare=lambda x: x or 0)

# Pct_Emp_Office_Svc,Pct_Educ_Svc,Pct_Medical_Svc,Pct_Public_Admin,
    percent_office_services = FloatField(prepare=lambda x: x or 0)
    percent_education_services = FloatField(prepare=lambda x: x or 0)
    percent_medical_services = FloatField(prepare=lambda x: x or 0)
    percent_public_admin = FloatField(prepare=lambda x: x or 0)

#Pct_Retail_Svc,Pct_Restuarant,Pct_Accommodation,Pct_Arts_Entertainment,Pct_Other_Svc,
    percent_retail_services = FloatField(prepare=lambda x: x or 0)
    percent_restaurant = FloatField(prepare=lambda x: x or 0)
    percent_accommodation = FloatField(prepare=lambda x: x or 0)
    percent_arts_entertainment = FloatField(prepare=lambda x: x or 0)
    percent_other_services = FloatField(prepare=lambda x: x or 0)

# Pct_Manufacturing,Pct_Transport_warehouse,Pct_Wholesale,Pct_Construction_Util,Pct_Agriculture,Pct_Extraction,
    percent_manufacturing = FloatField(prepare=lambda x: x or 0)
    percent_transport_warehouse = FloatField(prepare=lambda x: x or 0)
    percent_wholesale = FloatField(prepare=lambda x: x or 0)
    percent_construction_utilities = FloatField(prepare=lambda x: x or 0)

    percent_agriculture = FloatField(prepare=lambda x: x or 0)
    percent_extraction = FloatField(prepare=lambda x: x or 0)

# percent_of_building_type,floors,percent_residential,percent_retail,percent_office,percent_industrial,
    percent_of_placetype_component = FloatField(prepare=lambda x: x or 0)
    floors = FloatField(prepare=lambda x: x or 0)

    # percent_residential = FloatField(prepare=lambda x: x or 0)
    # percent_retail = FloatField(prepare=lambda x: x or 0)
    # percent_office = FloatField(prepare=lambda x: x or 0)
    # percent_industrial = FloatField(prepare=lambda x: x or 0)

#total_far,parking_spaces,parking_structure_square_feet,residential_efficiency,residential_lot_square_feet,square_feet_per_du,
    total_far = FloatField(prepare=lambda x: x or 0)
    parking_spaces = FloatField(prepare=lambda x: x or 0)
    parking_structure_square_feet = FloatField(prepare=lambda x: x or 0)

    residential_efficiency = FloatField(prepare=lambda x: x or 0)
    residential_average_lot_size = FloatField(prepare=lambda x: x or 0)
    residential_square_feet_per_unit = FloatField(prepare=lambda x: x or 0)

# retail_efficiency,retail_square_feet_per_employee,office_efficiency,office_square_feet_per_employee,
    retail_efficiency = FloatField(prepare=lambda x: x or 0)
    retail_square_feet_per_unit = FloatField(prepare=lambda x: x or 0)
    office_efficiency = FloatField(prepare=lambda x: x or 0)
    office_square_feet_per_unit = FloatField(prepare=lambda x: x or 0)

#industrial_efficiency,industrial_square_feet_per_employee,
    industrial_efficiency = FloatField(prepare=lambda x: x or 0)
    industrial_square_feet_per_unit = FloatField(prepare=lambda x: x or 0)

# misc_percent_of_retail_use,retail_percent_of_retail_use,restaurant_percent_of_retail_use,grocery_percent_of_retail_use,
    misc_percent_of_retail_use = FloatField(prepare=lambda x: x or 0)
    retail_percent_of_retail_use = FloatField(prepare=lambda x: x or 0)
    restaurant_percent_of_retail_use = FloatField(prepare=lambda x: x or 0)
    grocery_percent_of_retail_use = FloatField(prepare=lambda x: x or 0)

# hardscape_percent,irrigated_percent,impervious_roof_percent,impervious_hardscape_percent,pervious_hardscape_percent,softscape_landscape_percent,
    hardscape_percent = FloatField(prepare=lambda x: x or 0)
    irrigated_percent = FloatField(prepare=lambda x: x or 0)
    impervious_roof_percent = FloatField(prepare=lambda x: x or 0)
    impervious_hardscape_percent = FloatField(prepare=lambda x: x or 0)
    pervious_hardscape_percent = FloatField(prepare=lambda x: x or 0)
    softscape_and_landscape_percent = FloatField(prepare=lambda x: x or 0)

    id2 = IntegerField(prepare=lambda x: x or 0)

    class Meta:
        delimiter = ","
        has_header = True
