import logging

__author__ = 'calthorpe_associates'

from collections import OrderedDict
import unittest
import itertools
import csv

from django.db.models import Sum
from nose import with_setup
from django.template.defaultfilters import slugify

from footprint.main.initialization.built_form.built_form_importer import BuiltFormImporter
# from footprint.main.initialization.fixture import BuiltFormFixture
from footprint.main.mixins.building_aggregate import BuildingAttributeAggregate
from footprint.main.models.config.config_entity import ConfigEntity
from footprint.main.models.application_initialization import initialize_table_definitions, initialize_global_config
from footprint.main.models.built_form.primary_component import PrimaryComponent
from footprint.main.models.built_form.placetype_component import PlacetypeComponent
from footprint.main.models.built_form.placetype import Placetype
from footprint.main.models.built_form.flat_built_forms import refresh_all_flat_built_forms
from footprint.main.models.built_form.flat_built_forms import FlatBuiltForm
from footprint.main.models.config.global_config import global_config_singleton
from footprint.main.models.keys.keys import Keys
from footprint.main.publishing import built_form_publishing
from footprint.main.utils.utils import update_and_return_dict
from django.conf import settings

logger = logging.getLogger(__name__)
class TestBuiltFormExport(unittest.TestCase):
    """
    tests the export of the built forms
    """

    def setup(self):
        initialize_table_definitions()
        initialize_global_config()
        global_config = global_config_singleton()
        # built_form_publishing.on_config_entity_post_save_built_form(None, instance=ConfigEntity._subclassed_config_entity(global_config))
        # print "initializing data..."
        # initialize_table_definitions()
        # self.data_provider = DataProvider()
        # print "creating built forms"
        # client_built_form = resolve_fixture(
        #     "built_form",
        #     "built_form",
        #     BuiltFormFixture,
        #     settings.CLIENT)
        # self.built_forms_dict = client_built_form.built_forms()

    def teardown(self):
        pass

    def test_acres_parcel(self):
        self.setup()
        refresh_all_flat_built_forms()
        for built_form in FlatBuiltForm.objects.all():
            total_acres_parcel = sum([built_form.acres_parcel_employment,
                                     built_form.acres_parcel_residential,
                                     built_form.acres_parcel_mixed_use])
            if total_acres_parcel < .0001:
                logger.warn(built_form.built_form_type + '\t:' + built_form.name + ':' + str(total_acres_parcel))
            else:
                logger.debug(built_form.built_form_type + '\t:' + built_form.name + ':' + str(total_acres_parcel))

    def get_buildings_from_buildingtypes(self, buildingtype_names):
        test_buildings_dict = dict()
        building_percents = self.built_forms_dict['primary_component_percents']

        test_buildings_dict['primary_component_percents'] = [building_percent for building_percent in building_percents
                                                    if building_percent['buildingtype_name'] in buildingtype_names]
        test_buildings_dict['primary_components'] = [building_percent['building'] for building_percent in building_percents
                                            if building_percent['buildingtype_name'] in buildingtype_names]

        building_names = [building_percent['building_name'] for building_percent
                          in test_buildings_dict['primary_component_percents']]

        test_buildings_dict['building_use_percents'] = [use for use in self.built_forms_dict['building_use_percents']
                                                        if use['built_form_name'] in building_names]
        return test_buildings_dict

    def get_components_from_placetypes(self, placetype_names):
        test_buildingtypes_dict = dict()

        component_percents = test_buildingtypes_dict['placetype_component_percents'] = {}
        buildingtype_names = []
        for placetype in placetype_names:
            component_percents[placetype] = self.built_forms_dict['placetype_component_percents'][placetype]
            buildingtype_names.append([buildingtype for buildingtype, values
                                       in component_percents[placetype]['placetype_components'].items()])
        test_buildingtypes_dict['placetype_components'] = [buildingtype for buildingtype in component_percents]

        buildingtype_names = list(set([item for sublist in buildingtype_names for item in sublist]))
        test_buildingtypes_dict['placetype_components'] = [
            buildingtype for buildingtype in self.built_forms_dict['placetype_components']
            if buildingtype['building_attributes']['name'] in buildingtype_names]
        test_buildings_dict = self.get_buildings_from_buildingtypes(buildingtype_names)
        test_buildingtypes_dict.update(test_buildings_dict)

        return test_buildingtypes_dict

    def test_building_export(self, buildings_array):
        buildings_dict = self.built_forms_dict.copy()
        drop_values = ["primary_component_percents", "placetype_component_percents", "placetypes",
                       "sacog_placetypes", "building_percents"]

        building_names = [building['building_attributes']['name'] for building in buildings_array]
        for d in drop_values:
            buildings_dict[d] = {}

        buildings_dict['building_use_percents'] = [
            use for use in self.built_forms_dict['building_use_percents'] if use['built_form_name'] in building_names
        ]

        buildings_dict['primary_components'] = [building for building in buildings_dict['primary_components']
                                       if building['building_attributes']['name'] in building_names]

        self.data_provider.persist_built_forms(buildings_dict)
        self.test_flat_built_form_values()

    def test_buildingtype_export(self, buildingtype_array):
        test_buildingtypes_dict = self.built_forms_dict.copy()

        drop_values = "infrastructure_types", "placetype_component_percents", "placetypes", "sacog_placetypes"
        for d in drop_values:
            test_buildingtypes_dict[d] = {}

        test_buildingtypes_dict['placetype_components'] = buildingtype_array

        buildingtype_names = [buildingtype['building_attributes']['name'] for buildingtype in buildingtype_array]

        buildings_and_components_dict = self.get_buildings_from_buildingtypes(buildingtype_names)

        test_buildingtypes_dict.update(buildings_and_components_dict)
        self.data_provider.persist_built_forms(test_buildingtypes_dict)
        self.test_flat_built_form_values()

    def test_placetype_export(self, placetype_array):
        test_placetype_dict = self.built_forms_dict.copy()

        drop_values = ["sacog_placetypes"]

        for d in drop_values:
            test_placetype_dict[d] = {}
        test_placetype_dict['placetypes'] = placetype_array

        placetype_names = [placetype['building_attributes']['name'] for placetype in placetype_array]
        components_dict = self.get_components_from_placetypes(placetype_names)
        test_placetype_dict.update(components_dict)
        self.data_provider.persist_built_forms(test_placetype_dict)
        self.test_flat_built_form_values()

    def test_one_buildingtype_export(self):
        buildingtypes = [self.built_forms_dict['placetype_components'][0]]
        self.test_buildingtype_export(buildingtypes)

    def test_one_placetype_export(self):
        test_placetypes = [placetype for placetype in self.built_forms_dict['placetypes']
                           if placetype.name == 'Office/Industrial']
        self.test_placetype_export(test_placetypes)

    def test_all_placetype_exports(self):
        test_placetypes = self.built_forms_dict['placetypes']
        self.test_placetype_export(test_placetypes)

    def reasonably_close(self, value1, value2):
        return abs(value1 - value2) < .005

    def test_one_building_export(self):
        test_building = [self.built_forms_dict['primary_components'][0]]
        self.test_building_export(test_building)

    def test_all_building_exports(self):
        test_buildings = self.built_forms_dict['primary_components']
        self.test_building_export(test_buildings)

    def test_rural_employment_buildings(self):
        buildingtype_name = ["Rural Employment"]
        buildings = self.get_buildings_from_buildingtypes([buildingtype_name])['primary_components']
        self.test_building_export(buildings)

    def test_non_rural_employment_buildings(self):
        buildingtypes = [buildingtype['building_attributes']['name'] for buildingtype in self.built_forms_dict['placetype_components']
                         if buildingtype['building_attributes']['name'] != 'Rural Employment']
        buildings = self.get_buildings_from_buildingtypes(buildingtypes)['primary_components']
        self.test_building_export(buildings)

    def test_non_rural_employment_buildingtypes(self):
        buildingtypes = [buildingtype for buildingtype in self.built_forms_dict['placetype_components']
                         if buildingtype['building_attributes']['name'] != 'Rural Employment']
        self.test_buildingtype_export(buildingtypes)

    def test_non_rural_employment_placetypes(self):
        rural_placetype_names = [
            "Low Density Employment Park",
             "Rural Ranchettes",
             "Rural Employment",
             "Institutional",
             "Parks and Open Space"
        ]
        placetypes = [placetype for placetype in self.built_forms_dict['placetypes']]


    def test_flat_built_form_values(self):
        categories = (Keys.OFFICE_CATEGORY, Keys.OFFICE_SUBCATEGORIES), \
                     (Keys.AGRICULTURAL_CATEGORY, Keys.AGRICULTURAL_SUBCATEGORIES), \
                     (Keys.RETAIL_CATEGORY, Keys.RETAIL_SUBCATEGORIES), \
                     (Keys.RESIDENTIAL_CATEGORY, Keys.RESIDENTIAL_SUBCATEGORIES), \
                     (Keys.INDUSTRIAL_CATEGORY, Keys.INDUSTRIAL_SUBCATEGORIES)

        for building in PrimaryComponent.objects.all():
            building_uses = building.building_attributes.buildingusepercent_set.all()
            # checks that the major use categories have percents that are the sum of their subcategories
            for category, subcategory in categories:
                subcategories = building_uses.filter(building_use_definition__name__in=subcategory)
                if subcategories.exists():
                    subcategories_sum = subcategories.aggregate(Sum('percent'))['percent__sum']
                    category = building_uses.get(building_use_definition__name=category)
                    assert self.reasonably_close(category.percent, subcategories_sum)
                del category, subcategory, subcategories
            del building_uses

        print "exporting built forms to flat table..."
        refresh_all_flat_built_forms()
        assert FlatBuiltForm.objects.all().exists()
        print "checking data output of flat built forms..."
        for export_built_form in FlatBuiltForm.objects.all():

            report_dict = dict(
                built_form_name=export_built_form.__dict__['name'],
                clazz=export_built_form.built_form_type,
                condition="",
                operator="!=",
                value_1="",
                value_2=""
            )
            report_string = "*{clazz}* {built_form_name}: {condition} {value_1} {operator} {value_2}".format

            assert self.reasonably_close(export_built_form.residential_density, export_built_form.dwelling_unit_density), \
                report_string(**update_and_return_dict(report_dict, dict(
                    condition="residential density | unit density",
                    value_1=export_built_form.residential_density,
                    value_2=export_built_form.dwelling_unit_density)))

            top_level_categories_density_sum = sum([
                export_built_form.acres_parcel_employment,
                export_built_form.acres_parcel_residential,
                export_built_form.acres_parcel_mixed_use
            ])

            assert self.reasonably_close(top_level_categories_density_sum, export_built_form.gross_net_ratio), \
                report_string(**update_and_return_dict(report_dict, dict(
                    value_1=top_level_categories_density_sum,
                    operator='!=',
                    value_2=export_built_form.gross_net_ratio
                )))

            for employment_type in ['retail', 'office', 'industrial', 'agriculture']:
                if getattr(export_built_form, "acres_parcel_employment_{0}".format(employment_type), None) > 0:
                    assert getattr(export_built_form, "{0}_density".format(employment_type)) > 0, \
                        report_string(**update_and_return_dict(report_dict, dict(
                            operator="has no {0}_density, but does have acres_parcel_employment_{0}".format(
                                employment_type)
                        )))
            print report_string(**update_and_return_dict(report_dict, {'operator': "OK"}))

    @with_setup(setup, teardown)
    def test_example_creation(self):

        examples_file = 'placetype_examples.csv'
        # # Read in placetype examples and create a dictionary so you
        bf_examples_path = '%s/main/sproutcore/apps/fp/resources/Text/%s' % (settings.PROJECT_ROOT, examples_file)
        reader = csv.DictReader(open(bf_examples_path, "rU"))

        #This dictionary has builtform id's as the key, and the value is an array of dictionaries, each containing
        #data about an example area
        bf_examples = {}

        for row in reader:
            if row:
                pt__key = row["pt__key"]
                if bf_examples.get(pt__key):
                    bf_examples[pt__key].append(row)
                else:
                    bf_examples[pt__key] = [row]

        built_forms_dict = BuiltFormImporter().construct_built_forms('default')
        for placetype_dict in built_forms_dict['placetypes']:
            name = placetype_dict['building_attributes'].pop('name', None)

            placetype, created, updated = Placetype.objects.update_or_create(
                key='pt__' + slugify(name).replace('-', '_'),
                defaults=dict(
                    name=name,
                    intersection_density=placetype_dict['intersection_density'])
            )
            building_attributes_dict = placetype_dict['building_attributes']
            placetype.update_or_create_built_form_examples(bf_examples.get(placetype.key) if bf_examples.get(placetype.key) else [])

    def test_built_form_exports(self):
        """
        tests the built forms incrementally, so that problems that start with the building level of abstraction are
        identified before running the full suite of built form imports
        :return:
        """

        self.setup()
        self.test_flat_built_forms()
        print "All Built Forms passing tests!"

    def create_use_debug_dict(self, uses):
        return {use.building_use_definition.name: OrderedDict(
                unit_density=use.unit_density,
                floor_area_ratio=use.floor_area_ratio,
                vacancy_rate=use.vacancy_rate,
                percent=use.percent,
                )
                for use in uses}

    def create_component_debug_dict(self, components):
        return {component.component().name: OrderedDict(
            percent=component.percent,
            uses=self.create_use_debug_dict(component.component().building_attributes.buildingusepercent_set.all()))
            for component in components}

    def create_debug_dict(self, built_forms_dict):
        built_forms = itertools.chain(
            built_forms_dict['placetypes'].all(),
            built_forms_dict['placetype_components'].all(),
            built_forms_dict['primary_components'].all()
        )

        return {
            built_form.name: {
                'uses': self.create_use_debug_dict(built_form.building_attributes.buildingusepercent_set.all()),
                'components': self.create_component_debug_dict(built_form.get_all_components())
                if isinstance(built_form, BuildingAttributeAggregate) else None
            } for built_form in built_forms
        }

    def test_park_and_institutional(self):
        self.setup()
        placetypes = [placetype for placetype in self.built_forms_dict['placetypes']
                      if placetype['building_attributes']['name'] in ['Parks & Open Space']]
        self.test_placetype_export(placetypes)
        debug_dict = self.create_debug_dict(Placetype.objects.all())
        pass
        
    def test_rural_residential_types(self):
        self.setup()
        buildingtypes = [buildingtype for buildingtype in self.built_forms_dict['placetype_components']
                         if buildingtype['building_attributes']['name'] in ['Rural Ranchette', 'Rural Residential']]
        self.test_buildingtype_export(buildingtypes)

        debug_dict = self.create_debug_dict(PlacetypeComponent.objects.all())

        pass

    def get_flat_object(self, relational_object):
            return FlatBuiltForm.objects.get(built_form_id=relational_object.id)

    def test_flat_component_addition_of_attribute(self, aggregate, component_percents, attr):

        aggregate_attr = getattr(self.get_flat_object(aggregate), attr)

        sum_of_component_attributes = sum([
            getattr(self.get_flat_object(component_percent.component()), attr) * component_percent.percent
            for component_percent in component_percents
        ])

        error_dict = {
            'sum_of_components': sum_of_component_attributes,
            'aggregate': aggregate_attr,
            'error': abs(sum_of_component_attributes - aggregate_attr) / sum_of_component_attributes
            if sum_of_component_attributes else None,
        }

        # assert self.reasonably_close(sum_of_component_attributes, aggregate_attr)
        return error_dict

    def test_sum_of_uses(self, built_form):
        built_form_uses=list(built_form.building_attributes.buildingusepercent_set.all())
        sum_of_percents = sum([use.percent for use in built_form_uses])
        if not self.reasonably_close(sum_of_percents, 2):
            return dict(use_percent_totals=sum_of_percents,
                        uses=built_form_uses)
        return {}
        
    def test_primary_component_csv(self, client):
        error_dict = {}
        buildings = BuiltFormImporter().load_buildings_csv(client)

        for building in buildings:
            sum_of_uses = sum([
                building.percent_single_family_large_lot,
                building.percent_single_family_small_lot,
                building.percent_attached_single_family,
                building.percent_multifamily_2_to_4,
                building.percent_multifamily_5_plus,

                building.percent_office_services,
                building.percent_education_services,
                building.percent_medical_services,
                building.percent_public_admin,

                building.percent_retail_services,
                building.percent_restaurant,
                building.percent_accommodation,
                building.percent_arts_entertainment,
                building.percent_other_services,

                building.percent_manufacturing,
                building.percent_transport_warehouse,
                building.percent_wholesale,
                building.percent_construction_utilities,

                building.percent_agriculture,
                building.percent_extraction])

            if not self.reasonably_close(sum_of_uses, 1):
                error_dict[building.name] = sum_of_uses
        return error_dict



    def test_flat_built_forms(self):

        # client_import_errors = self.test_primary_component_csv('sacog')
        default_import_errors = self.test_primary_component_csv('default')
        self.setup()
        refresh_all_flat_built_forms()
        error_dict = {'primary_components': {}, 'placetype_components': {}, 'placetypes': {}}
        passing_dict = {'primary_components': [], 'placetype_components': [], 'placetypes': []}

        basic_test_attributes = ['residential_density', 'employment_density', 'building_sqft_total']

        for primary_component in PrimaryComponent.objects.all():
            use_error = self.test_sum_of_uses(primary_component)

            if use_error:
                error_dict['primary_components'][primary_component.name] = {'use_error': use_error,}

        placetype_components_error_dict = {}
        for placetype_component in PlacetypeComponent.objects.all():
            primary_component_percents = placetype_component.primarycomponentpercent_set.all()
            attribute_error_dict = {}

            for test_attr in basic_test_attributes:

                attribute_summing = self.test_flat_component_addition_of_attribute(
                    placetype_component, primary_component_percents, test_attr)

                if attribute_summing['error'] >= 0.00001:
                    attribute_error_dict[test_attr] = attribute_summing

            use_error = self.test_sum_of_uses(placetype_component)
            if use_error:
                attribute_error_dict['use_error'] = use_error

            if attribute_error_dict:
                placetype_components_error_dict[placetype_component.name] = attribute_error_dict
            elif placetype_component.name not in passing_dict['placetype_components']:
                passing_dict['placetype_components'].append(placetype_component.name)
        error_dict['placetype_components'] = placetype_components_error_dict

        for placetype in Placetype.objects.all():
            placetype_components = placetype.placetypecomponentpercent_set.all()

            for test_attr in basic_test_attributes:
                attribute_summing = self.test_flat_component_addition_of_attribute(placetype, placetype_components, test_attr)
                if attribute_summing['error'] > 0.00001:
                    if placetype.name not in error_dict['placetypes']:
                         error_dict['placetypes'][placetype.name] = {}
                    error_dict['placetypes'][placetype.name][test_attr] = attribute_summing
                elif placetype.name not in passing_dict['placetypes']:
                    passing_dict['placetypes'].append(placetype.name)

        return passing_dict, error_dict