# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
from collections import defaultdict
import csv
import importlib
import os
from footprint.initialization.built_form.built_form_derivatives import BuiltFormDerivatives
from footprint.initialization.built_form.import_primary_component import ImportPrimaryComponent
from footprint.initialization.built_form.import_placetype import ImportedPlacetype
from footprint.lib.functions import map_to_dict
from footprint.models import Placetype, PlacetypeComponentPercent, BuildingUsePercent, \
    PrimaryComponentPercent, PrimaryComponent, PlacetypeComponent
from settings import CLIENT




class BuiltFormImporter(BuiltFormDerivatives):
    def __init__(self):
        super(BuiltFormImporter, self).__init__()
        self.dir = os.path.dirname(__file__)

    def built_form_path(self, client):
        client_built_form_path = "{here}/../fixtures/client/{client}/built_form/import_csv".format(
            here=self.dir, client=client)

        return client_built_form_path

    def load_buildings_csv(self, client):
        """
        :param self.dir csv file self.directory
        :return: ImportedBuilding objects imported from UrbanFootprint v0.1 Built Form default set, csv or a custom
        set defined for the client
        """
        # Load building attribute data from a csv and used it to create Building instances
        path = '{0}/buildings.csv'.format(self.built_form_path(client))
        if not os.path.exists(path):
            return []
        file = open(path, "rU")
        imported_buildings = ImportPrimaryComponent.import_from_file(file) #import_from_filename(path)
        return imported_buildings

    def load_buildingtype_csv(self, client):
        """
        :return: ImportedBuildingtype objects imported from UrbanFootprint v0.1 Built Form default set, csv or a custom
        set defined for the client
        """
        if not os.path.exists(self.built_form_path(client)):
            return []
        client_built_form = "footprint.initialization.fixtures.client.{0}.built_form.{0}_import_placetype_component".format(client)
        importer_module = importlib.import_module(client_built_form)
        placetype_component_importer = importer_module.ImportPlacetypeComponent
        imported_buildingtypes = placetype_component_importer.import_from_filename(
            '{0}/buildingtypes.csv'.format(self.built_form_path(client)))
        return imported_buildingtypes

    def load_placetype_csv(self, client):
        """
        :return: ImportedPlacetype objects imported from UrbanFootprint v0.1 Built Form default set, csv or a custom
        set defined for the client
        """
        if not os.path.exists(self.built_form_path(client)):
            return []
        imported_placetypes = ImportedPlacetype.import_from_filename(
            '{0}/placetypes.csv'.format(self.built_form_path(client)))
        return imported_placetypes

    def construct_primary_components(self, client='default'):
        """
        :return: Dictionary keyed by Building name and valued by Building objects (UrbanFootprint v0.1 Built
        Form default set)
        """
        primary_components = []

        for import_primary_component in self.load_buildings_csv(client):
            building_attributes = dict(
                name=import_primary_component.name,
                floors=import_primary_component.floors,
                total_far=import_primary_component.total_far,
                softscape_and_landscape_percent=import_primary_component.softscape_and_landscape_percent,
                pervious_hardscape_percent=import_primary_component.pervious_hardscape_percent,
                impervious_hardscape_percent=import_primary_component.impervious_hardscape_percent,
                impervious_roof_percent=import_primary_component.impervious_roof_percent,
                parking_structure_square_feet=import_primary_component.parking_structure_square_feet,
                parking_spaces=import_primary_component.parking_spaces,
                residential_average_lot_size=import_primary_component.residential_average_lot_size,
                irrigated_percent=import_primary_component.irrigated_percent,
            )

            primary_component = dict(building_attributes=building_attributes)

            primary_components.append(primary_component)

        return map_to_dict(lambda primary_component:
                           [primary_component['building_attributes']['name'], primary_component],
                           primary_components)

    def construct_placetype_components(self, client):
        """
        :return: A dict keyed by BuildingType name and valued by BuildingType objects (UrbanFootprint v0.1 Built Form
        default set)
        """
        placetype_component_names = []
        placetype_components = []
        placetype_component_imports = self.load_buildingtype_csv(client)
        for b in placetype_component_imports:
            placetype_components.append(dict(
                name=b.name,
                color=b.color,
                component_category=b.category
            ))

        for placetype_component_name in set(placetype_component_names):
            building_attributes = dict(name=placetype_component_name)
            placetype_components.append(dict(building_attributes=building_attributes))

        return map_to_dict(lambda placetype_component:
                           [placetype_component['name'], placetype_component],
                           placetype_components)

    def construct_placetypes(self, client):
        """
        :return: PlaceType objects (UrbanFootprint v0.1 Built Form default set)
        """

        placetypes = []
        for placetype in self.load_placetype_csv(client):
            building_attributes = dict(name=placetype.name)
            placetype = dict(
                building_attributes=building_attributes,
                color=placetype.color,
                intersection_density=placetype.intersection_density
            )
            placetypes.append(placetype)
        return map_to_dict(
            lambda placetype: [placetype['building_attributes']['name'], placetype], placetypes)


    def construct_built_forms(self, client):
        """
        Calls all the functions necessary to generate the Built Forms to mimic the
        starter set of v0.1 UrbanFootprint Built Forms
         """
        if not os.path.exists(self.built_form_path(client)):
            return {}

        built_form_dict = dict(
            primary_component_lookup=self.construct_primary_components(client),
            placetype_component_lookup=self.construct_placetype_components(client),
            placetype_lookup=self.construct_placetypes(client)
        )

        primary_component_lookup = built_form_dict['primary_component_lookup']

        return {
            'placetypes': built_form_dict['placetype_lookup'].values(),
            'placetype_components': built_form_dict['placetype_component_lookup'].values(),
            'primary_components': primary_component_lookup.values(),
            'primary_component_percents': self.construct_primary_component_percents(
                built_form_dict['placetype_component_lookup'],
                primary_component_lookup,
                client=client),
            'building_use_percents': self.construct_building_use_percents(primary_component_lookup, client=client),
            'placetype_component_percents': self.construct_placetype_component_percents(
                built_form_dict['placetype_lookup'],
                built_form_dict['placetype_component_lookup'], client=client),
        }


    def construct_sample_built_forms(self, client):
        """
        Builds a sample set of built forms for testing
        """
        placetypes = self.construct_sample_placetypes()
        buildingtypes = self.construct_sample_placetype_components(placetypes)

        building_percents = self.construct_sample_primary_component_percents(buildingtypes)

        buildings = [building['building'] for building in building_percents]
        building_dict = map_to_dict(lambda building: [building['building_attributes']['name'], building], buildings)
        buildingtype_dict = map_to_dict(
            lambda buildingtype: [buildingtype['building_attributes']['name'], buildingtype], buildingtypes)

        return {'placetypes': placetypes,
                'placetype_components': buildingtypes,
                'primary_components': buildings,
                'primary_component_percents': building_percents,
                'building_use_percents': self.construct_building_use_percents(building_dict, client=client),
                'placetype_component_percents': self.construct_placetype_component_percents(
                    map_to_dict(lambda placetype: [placetype['building_attributes']['name'], placetype], placetypes),
                    buildingtype_dict, client=client)}


    def construct_sample_placetypes(self):
        """
        :return: a sample set of four placetypes
        """
        pt_ids = [1, 2, 3, 8, 9, 10, 16, 20, 25, 29, 30]
        sample_placetypes = list(self.construct_placetypes(client='default')[i] for i in pt_ids)

        return sample_placetypes


    def construct_sample_placetype_components(self, sample_placetypes):
        sample_placetype_components = []
        all_placetype_components = self.construct_placetype_components(client='default')
        placetype_component_dict = map_to_dict(
            lambda placetype_component: [placetype_component['building_attributes']['name'], placetype_component],
            all_placetype_components
        )

        sample_buildingtype_percents = self.construct_placetype_component_percents(
            map_to_dict(lambda placetype: [placetype['building_attributes']['name'], placetype], sample_placetypes),
            placetype_component_dict)

        placetype_components = []
        for placetype, components in sample_buildingtype_percents.items():
            for placetype_components, attributes in components['placetype_components'].items():
                placetype_components.append(placetype_components)

        for placetype_components in set(placetype_components):
            sample_placetype_components.append({'building_attributes': {'name': placetype_components}})

        return sample_placetype_components

    def construct_sample_primary_component_percents(self, sample_placetype_components, client):
        all_primary_components = self.construct_primary_components()
        primary_component_dict = map_to_dict(lambda building: [building['building_attributes']['name'], building],
                                             all_primary_components)

        sample_placetype_component_dict = map_to_dict(
            lambda placetype_component: [placetype_component['building_attributes']['name'], placetype_component],
            sample_placetype_components
        )
        sample_primary_component_percents = []

        for import_primary_component in self.load_buildings_csv(client):
            component = import_primary_component.placetype_component
            if component not in sample_placetype_component_dict:
                print "BuildingType " + import_primary_component.placetype + " is not used in this set :: skipping"
                continue

            placetype_component = sample_placetype_component_dict[component]
            building_percent = dict(
                primary_component_name=import_primary_component.name,
                primary_component=primary_component_dict[import_primary_component.name],
                placetype_component_name=import_primary_component.building_type,
                placetype_component=placetype_component,
                percent=import_primary_component.percent_of_building_type
            )
            sample_primary_component_percents.append(building_percent)

        return sample_primary_component_percents


    def delete_built_forms(self):
        """
        Deletes all BuiltForm objects from the database.
        """

        Placetype.objects.all().delete()
        PlacetypeComponentPercent.objects.all().delete()
        BuildingUsePercent.objects.all().delete()
        PrimaryComponentPercent.objects.all().delete()
        PrimaryComponent.objects.all().delete()
        PlacetypeComponent.objects.all().delete()
        PlacetypeComponentPercent.objects.all().delete()
