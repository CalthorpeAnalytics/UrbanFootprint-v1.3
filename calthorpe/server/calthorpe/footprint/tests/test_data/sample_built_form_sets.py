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
import os
from collections import defaultdict
from footprint.models import PlacetypeComponent, PrimaryComponent
from footprint.models.built_form.placetype_component import PlacetypeComponentCategory

from footprint.tests.test_data.imported_building import ImportedBuilding
from footprint.tests.test_data.imported_buildingtype import ImportedBuildingtype, ImportedPlacetypes

from footprint.lib.functions import map_to_dict
from footprint.models.built_form.building_use_definition import BuildingUseDefinition
from footprint.models.built_form.placetype import Placetype

from footprint.models.keys.keys import Keys
from footprint.utils.utils import get_or_none

__author__ = 'calthorpe'

#def construct_built_forms():
#    buildtype_data = construct_buildingtypes()
#    return merge(buildtype_data, construct_placetypes(buildtype_data['buildingtypes']))

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

def load_buildings_csv():
    """
    :return: ImportedBuilding objects imported from UrbanFootprint v0.1 Built Form default set, csv
    """
    # Load building attribute data from a csv and used it to create Building instances
    dir = os.path.dirname(__file__)
    imported_buildings = ImportedBuilding.import_from_filename('{0}/buildings_with_subcategories.csv'.format(dir))

    # this is a fix, because the top level categories in the source csv are sometimes wrong. we recalculate those top-level
    # categories here

    for building in imported_buildings:
        building.percent_retail = sum(
            [building.percent_retail_services, building.percent_restaurant, building.percent_accommodation,
             building.percent_arts_entertainment, building.percent_other_services]
        )
        building.percent_industrial = sum(
            [building.percent_manufacturing, building.percent_transport_warehouse, building.percent_wholesale,
             building.percent_construction_utilities, building.percent_agriculture, building.percent_extraction]
        )
        building.percent_residential = sum(
            [building.percent_single_family_large_lot, building.percent_single_family_small_lot,
            building.percent_attached_single_family, building.percent_multifamily_2_to_4,
            building.percent_multifamily_5_plus]
        )
        building.percent_office = sum(
            [building.percent_office_services, building.percent_education_services, building.percent_medical_services,
             building.percent_public_admin]
        )

    return imported_buildings

def load_buildingtype_csv():
    """
    :return: ImportedBuildingtype objects imported from UrbanFootprint v0.1 Built Form default set, csv
    """
    dir = os.path.dirname(__file__)
    imported_buildingtypes = ImportedBuildingtype.import_from_filename('{0}/buildingtypes.csv'.format(dir))
    return imported_buildingtypes

def load_placetype_csv():
    """
    :return: ImportedPlacetype objects imported from UrbanFootprint v0.1 Built Form default set, csv
    """
    dir = os.path.dirname(__file__)
    imported_placetypes = ImportedPlacetypes.import_from_filename('{0}/placetypes.csv'.format(dir))
    return imported_placetypes

# By default we create a BuiltFormSet for each class, one for Placetypes, BuildingTypes, and Buildings.
# Sets can contain instances of multiple classes, but this is the configuration is easiest to understand
def built_form_sets():
    # Configuration for BuiltFormSets
    return [
        dict(
            key='placetype',
            name='Placetypes',
            description='BuiltFormSet containing only placetypes',
            clazz=Placetype
        ),
        dict(
            key='buildingtype',
            name='Buildingtypes',
            description='BuiltFormSet containing only buildingtypes',
            clazz=PlacetypeComponent
        ),
        dict(
            key='building',
            name='Buildings',
            description='BuiltFormSet containing only buildings',
            clazz=PrimaryComponent
        )
    ]

def construct_buildings():
    """
    :return: Building objects (UrbanFootprint v0.1 Built Form default set)
    """
    buildings = []

    for import_building in load_buildings_csv():

        building_attributes = dict(
            name=import_building.name,
            floors=import_building.floors,
            total_far=import_building.total_far,
            softscape_and_landscape_percent=import_building.softscape_and_landscape_percent,
            pervious_hardscape_percent=import_building.pervious_hardscape_percent,
            impervious_hardscape_percent=import_building.impervious_hardscape_percent,
            impervious_roof_percent=import_building.impervious_roof_percent,
            parking_structure_square_feet=import_building.parking_structure_square_feet,
            parking_spaces=import_building.parking_spaces,
            residential_average_lot_size=import_building.residential_average_lot_size,
            irrigated_percent=import_building.irrigated_percent,
        )

        building = dict(building_attributes=building_attributes)

        buildings.append(building)

    return buildings


def construct_buildingtypes():
    """
    :return: BuildingType objects (UrbanFootprint v0.1 Built Form default set)
    """
    buildingtype_names = []
    buildingtypes = []

    for b in load_buildings_csv():
        buildingtype_names.append(b.building_type)

    for buildingtype_name in set(buildingtype_names):
        building_attributes = dict(name=buildingtype_name)
        buildingtypes.append(dict(building_attributes=building_attributes))

    return buildingtypes


def construct_placetypes():
    """
    :return: PlaceType objects (UrbanFootprint v0.1 Built Form default  set)
    """
    placetypes = []
    for placetype in load_placetype_csv():
        building_attributes = dict(name=placetype.name)
        placetype = dict(building_attributes=building_attributes, color=placetype.color)
        placetypes.append(placetype)
    return placetypes


def construct_building_percents(buildingtypes, buildings):
    """
    :return: BuildingPercent objects (UrbanFootprint v0.1 Built Form default set)
    """
    building_percents = []
    for import_building in load_buildings_csv():
        building_percent = dict(
            building_name=import_building.name,
            building=buildings[import_building.name],
            buildingtype_name=import_building.building_type,
            buildingtype=buildingtypes[import_building.building_type],
            percent=import_building.percent_of_building_type
        )
        building_percents.append(building_percent)
    return building_percents


def construct_building_use_percents(buildings):
    """
    :return: BuildingUsePercent objects (UrbanFootprint v0.1 Built Form default set)
    """
    building_use_percents = []

    def make_building_use_percent_dict(import_building, building_use, building_use_category):
        if building_use == 'Armed Forces':
            return None
        import_use_field = building_use.lower().replace(' ', '_')
        import_use_category_field = building_use_category.lower().replace(' ', '_')
        use_percent = getattr(import_building, 'percent_{0}'.format(import_use_field))
        if use_percent > 0:

            try:
                efficiency = getattr(import_building, '{0}_efficiency'.format(import_use_category_field))
                square_feet_per_unit = getattr(import_building, '{0}_square_feet_per_unit'.format(import_use_category_field))

            except:
                efficiency = 1
                square_feet_per_unit = 10000

            building_use_definition, created, updated = BuildingUseDefinition.objects.update_or_create(name=building_use)

            if not building_use_definition:
                return None

            building_uses = dict(
                building_use_definition=BuildingUseDefinition.objects.get(name=building_use),
                percent=use_percent,
                efficiency=efficiency,
                square_feet_per_unit=square_feet_per_unit,
            )

            building_use_percent = dict(
                built_form_dict=building,
                built_form_name=building['building_attributes']['name'],
                built_form_uses=building_uses
            )

            return building_use_percent

    for import_building in load_buildings_csv():
        if import_building.name not in buildings:
            continue
        category_sums = defaultdict(float)
        building = buildings[import_building.name]
        for building_use, building_use_category in Keys.BUILDING_USE_DEFINITION_CATEGORIES.items():
            building_use_percent = make_building_use_percent_dict(import_building, building_use, building_use_category)
            if building_use_percent:
                category_dict = category_sums[building_use_category] = defaultdict(float)
                building_use_percents.append(building_use_percent)
                category_dict['percent'] += building_use_percent['built_form_uses']['percent']
            del building_use_percent

    return building_use_percents


def construct_placetype_component_percents(placetype_dict, buildingtype_dict):
    """
    :return:
    """

    input_buildingtypes = load_buildingtype_csv()

    buildingtypes = []
    for buildingtype in input_buildingtypes:
        if buildingtype.gross_net_flag == 'Gross':
            buildingtypes.append(buildingtype)

    input_placetypes = load_placetype_csv()
    input_placetype_dict = map_to_dict(lambda input_placetype: [input_placetype.name, input_placetype], input_placetypes)
    placetype_component_percents = []
    placetype_component_dict = dict()

    for name, placetype in placetype_dict.items():

        for input_buildingtype in buildingtypes:

            placetype_name = placetype['building_attributes']['name'].strip()

            placetype_component_percent = getattr(input_buildingtype, input_placetype_dict[placetype_name].clean_name)
            placetype_component_name = input_buildingtype.name.strip()

            default_placetype_component_dict = {'buildingtypes': {}, 'infrastructuretypes': {}, }

            placetype_component_dict[placetype_name] = placetype_component_dict.get(placetype_name,
                                                                                    default_placetype_component_dict)

            if placetype_component_percent > 0:
                if placetype_component_name.strip() in Keys.INFRASTRUCTURE_TYPES:
                    placetype_component_dict[placetype_name]['infrastructuretypes'][placetype_component_name] = {
                        'percent': placetype_component_percent,
                    }
                else:
                    category = get_or_none(PlacetypeComponentCategory, name=input_buildingtype.category.strip)
                    if category:
                        placetype_component_dict[placetype_name]['buildingtypes'][placetype_component_name] = {
                            'category': category,
                            'percent': placetype_component_percent,
                        }

    return placetype_component_dict

def construct_built_forms():
    """
    Calls all the functions necessary to generate the Built Forms to mimic the
    starter set of v0.1 UrbanFootprint Built Forms
     """
    buildings = construct_buildings()
    buildingtypes = construct_buildingtypes()
    placetypes = construct_placetypes()
    building_dict = map_to_dict(lambda building: [building['building_attributes']['name'], building], buildings)
    buildingtype_dict = map_to_dict(lambda buildingtype: [buildingtype['building_attributes']['name'], buildingtype], buildingtypes)

    return {'placetypes': placetypes,
            'buildingtypes': buildingtypes,
            'buildings': buildings,
            'building_percents': construct_building_percents(buildingtype_dict, building_dict),
            'building_use_percents': construct_building_use_percents(building_dict),
            'placetype_component_percents': construct_placetype_component_percents(
                map_to_dict(lambda placetype: [placetype['building_attributes']['name'], placetype], placetypes),
                buildingtype_dict)}


def construct_sample_built_forms():
    """
    Builds a sample set of built forms for testing
    """
    placetypes = construct_sample_placetypes()
    buildingtypes = construct_sample_buildingtypes(placetypes)

    building_percents = construct_sample_building_percents(buildingtypes)

    buildings = [building['building'] for building in building_percents]
    building_dict = map_to_dict(lambda building: [building['building_attributes']['name'], building], buildings)
    buildingtype_dict = map_to_dict(lambda buildingtype: [buildingtype['building_attributes']['name'], buildingtype], buildingtypes)

    return {'placetypes': placetypes,
            'buildingtypes': buildingtypes,
            'buildings': buildings,
            'building_percents': building_percents,
            'building_use_percents': construct_building_use_percents(building_dict),
            'placetype_component_percents': construct_placetype_component_percents(
                map_to_dict(lambda placetype: [placetype['building_attributes']['name'], placetype], placetypes),
                buildingtype_dict)}


def construct_sample_placetypes():
    """
    :return: a sample set of four placetypes
    """
    sample_placetypes = list(construct_placetypes()[i] for i in [1, 2, 3, 8, 9, 10, 16, 20, 25, 29, 30])

    return sample_placetypes


def construct_sample_buildingtypes(sample_placetypes):
    sample_buildingtypes = []
    all_buildingtypes = construct_buildingtypes()
    buildingtype_dict = map_to_dict(
        lambda buildingtype: [buildingtype['building_attributes']['name'], buildingtype], all_buildingtypes
    )

    sample_buildingtype_percents = construct_placetype_component_percents(
        map_to_dict(lambda placetype: [placetype['building_attributes']['name'], placetype], sample_placetypes),
        buildingtype_dict)

    buildingtypes = []
    for placetype, components in sample_buildingtype_percents.items():
        for buildingtype, attributes in components['buildingtypes'].items():
            buildingtypes.append(buildingtype)

    for buildingtype in set(buildingtypes):
        sample_buildingtypes.append({'building_attributes': {'name': buildingtype}})

    return sample_buildingtypes


def construct_sample_building_percents(sample_buildingtypes):
    all_buildings = construct_buildings()
    building_dict = map_to_dict(lambda building: [building['building_attributes']['name'], building], all_buildings)

    sample_buildingtype_dict = map_to_dict(lambda buildingtype: [buildingtype['building_attributes']['name'], buildingtype], sample_buildingtypes)
    sample_building_percents = []

    for import_building in load_buildings_csv():
        if import_building.building_type not in sample_buildingtype_dict:
            print "BuildingType " + import_building.building_type + " is not used in this set :: skipping"
            continue

        buildingtype = sample_buildingtype_dict[import_building.building_type]
        building_percent = dict(
            building_name=import_building.name,
            building=building_dict[import_building.name],
            buildingtype_name=import_building.building_type,
            buildingtype=buildingtype,
            percent=import_building.percent_of_building_type
        )
        sample_building_percents.append(building_percent)


    return sample_building_percents