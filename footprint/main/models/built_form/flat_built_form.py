# coding=utf-8

import math
import logging
from collections import defaultdict
from django.db.models import Sum
from django.template.defaultfilters import slugify
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.built_form.built_form import BuiltForm
from footprint.main.models.built_form.urban.building_type import BuildingType
from footprint.main.models.built_form.urban.building import Building
from footprint.main.models.built_form.urban.urban_placetype import UrbanPlacetype
from footprint.main.models.keys.keys import Keys


__author__ = 'calthorpe_associates'

from django.db import models
logger = logging.getLogger(__name__)


class FlatBuiltForm(models.Model):
    objects = GeoInheritanceManager()
    built_form_id = models.IntegerField(null=False, primary_key=True)
    key = models.CharField(max_length=120)

    intersection_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)

    name = models.CharField(max_length=100)
    built_form_type = models.CharField(max_length=50)
    gross_net_ratio = models.DecimalField(max_digits=11, decimal_places=10, default=0)

    # top level category densities
    dwelling_unit_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    household_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    population_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    employment_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)

    # subcategory densities
    single_family_large_lot_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    single_family_small_lot_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    attached_single_family_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    multifamily_2_to_4_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    multifamily_5_plus_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)

    retail_services_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    restaurant_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    arts_entertainment_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    accommodation_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    other_services_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)

    office_services_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    public_admin_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    education_services_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    medical_services_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)

    manufacturing_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    wholesale_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    transport_warehouse_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    construction_utilities_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)

    agriculture_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    extraction_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)

    armed_forces_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)

    office_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    retail_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    industrial_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    residential_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    agricultural_density = models.DecimalField(max_digits=15, decimal_places=10, default=0)

    # acres parcel fields: these could be modeled more nicely, but this is fine for now
    acres_parcel_mixed_use = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    acres_parcel_residential = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    acres_parcel_employment = models.DecimalField(max_digits=15, decimal_places=10, default=0)

    acres_parcel_mixed_use_with_office = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    acres_parcel_mixed_use_without_office = models.DecimalField(max_digits=15, decimal_places=10, default=0)

    acres_parcel_residential_single_family_small_lot = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    acres_parcel_residential_single_family_large_lot = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    acres_parcel_residential_attached_single_family = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    acres_parcel_residential_multifamily = models.DecimalField(max_digits=15, decimal_places=10, default=0)

    acres_parcel_employment_office = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    acres_parcel_employment_retail = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    acres_parcel_employment_industrial = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    acres_parcel_employment_agriculture = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    acres_parcel_employment_mixed = models.DecimalField(max_digits=15, decimal_places=10, default=0)

    # building square feet fields
    building_sqft_total = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_detached_single_family = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_single_family_small_lot = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_single_family_large_lot = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_attached_single_family = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_multifamily_2_to_4 = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_multifamily_5_plus = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_retail_services = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_restaurant = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_accommodation = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_arts_entertainment = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_other_services = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_office_services = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_public_admin = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_education_services = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_medical_services = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_wholesale = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_transport_warehouse = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    building_sqft_industrial_non_warehouse = models.DecimalField(max_digits=15, decimal_places=7, default=0)

    residential_irrigated_square_feet = models.DecimalField(max_digits=15, decimal_places=7, default=0)
    commercial_irrigated_square_feet = models.DecimalField(max_digits=15, decimal_places=7, default=0)

    softscape_and_landscape_percent = models.DecimalField(max_digits=15, decimal_places=7, null=True)
    irrigated_percent = models.DecimalField(max_digits=15, decimal_places=7, default=0, null=True)

    # other fields not used for the core but useful in placetype visualization
    percent_streets = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    percent_parks = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    percent_civic = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    percent_mixed_use = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    percent_residential = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    percent_employment = models.DecimalField(max_digits=6, decimal_places=5, default=0)

    pt_density = models.IntegerField(null=True)
    pt_connectivity = models.IntegerField(null=True)
    pt_land_use_mix = models.IntegerField(null=True)
    pt_score = models.IntegerField(null=True)

    description = models.TextField(null=True, blank=True)

    intersections_sqmi = models.IntegerField(null=True)
    avg_estimated_building_height_feet = models.IntegerField(null=True)
    building_avg_number_of_floors = models.IntegerField(null=True)
    block_avg_size_acres = models.IntegerField(null=True)
    street_pattern = models.CharField(max_length=100, null=True)

    combined_pop_emp_density = models.DecimalField(max_digits=14, decimal_places=4, default=0, null=True)

    class Meta(object):
        abstract = False
        app_label = 'main'

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name

    def collect_built_form_attributes(self):
        """
        Navigates the relational model describing built form and collects the critical data into a flat dictionary
        describing all the attributes of a single built form, in a way that parallels the data required by the core v1
        :return: dict of built form attributes
        """
        built_form = BuiltForm.resolve_built_form_by_id(self.built_form_id)
        built_form_uses = built_form.building_attribute_set.buildingusepercent_set.all()

        type = built_form.__class__.__name__
        key_prepend = 'b__' if type == 'Building' else 'bt__' if type == "BuildingType" else "pt__"
        building_attribute_set = built_form.building_attribute_set
        if not building_attribute_set:
            raise Exception("No attributes for " + built_form)
        built_form_dict = {
            'basic_attributes': {
                'name': built_form.name,
                'key': key_prepend + slugify(built_form.name).replace('-', '_'),
                'built_form_type': type,
                'gross_net_ratio': building_attribute_set.gross_net_ratio,
                'intersection_density': built_form.intersection_density if isinstance(built_form, UrbanPlacetype) else 0
            },
            'density': defaultdict(float),
            'parcel_acres': defaultdict(float),
            'building_square_feet': defaultdict(float),
            'irrigation': defaultdict(float),
            'residential_attributes': {
                'hh_avg_size': building_attribute_set.household_size,
                'vacancy_rate': building_attribute_set.vacancy_rate}
        }
        built_form_uses = list(built_form_uses.values_list('building_use_definition__name', flat=True))

        # do parcel acres first
        if built_form.__class__ in [BuildingType, Building]:
            built_form_dict['parcel_acres'] = create_parcel_acres_dict(built_form, built_form_uses)

        if built_form.__class__ == UrbanPlacetype:

            parcel_acres_dict = defaultdict(float)

            for component_percent in built_form.placetypecomponentpercent_set.filter():
                component = component_percent.component()
                uses = component.building_attribute_set.buildingusepercent_set.all()
                component_use_names = list(uses.values_list('building_use_definition__name', flat=True))
                component_parcel_acres_dict = create_parcel_acres_dict(component, component_use_names)

                for key, value in component_parcel_acres_dict.items():
                    parcel_acres_dict[key] += value * float(component_percent.percent)

            built_form_dict['parcel_acres'] = parcel_acres_dict

        for use in Keys.RESIDENTIAL_SUBCATEGORIES + Keys.COMMERCIAL_SUBCATEGORIES:
            use_name = use.lower().replace(' ', '_')
            if use in built_form_uses:
                use_list = [use]
                for active_use in building_attribute_set.buildingusepercent_set.filter(building_use_definition__name__in=use_list):
                    built_form_dict['building_square_feet']['building_sqft_' + use_name] = active_use.gross_built_up_area
            else:
                built_form_dict['building_square_feet']['building_sqft_' + use_name] = 0


        for use in Keys.RESIDENTIAL_SUBCATEGORIES + Keys.COMMERCIAL_SUBCATEGORIES:
            use_name = use.lower().replace(' ', '_')
            if use in built_form_uses:
                use_list = [use]
                for active_use in building_attribute_set.buildingusepercent_set.filter(building_use_definition__name__in=use_list):
                    built_form_dict['density'][use_name + "_density"] = 0 \
                        if active_use.square_feet_per_unit == 0 or building_attribute_set.lot_size_square_feet == 0 else active_use.unit_density
            else:
                built_form_dict['density'][use_name + "_density"] = 0

        irrigation_dict = built_form_dict['irrigation']

        irrigation_dict['irrigated_percent'] = building_attribute_set.irrigated_percent
        irrigation_dict['residential_irrigated_square_feet'] = building_attribute_set.residential_irrigated_square_feet or 0
        irrigation_dict['commercial_irrigated_square_feet'] = building_attribute_set.commercial_irrigated_square_feet or 0

        return built_form, built_form_dict


    def update_attributes(self):
        """
        updates the flat representation of a built form. should be executed whenever any part of the built form
        has been changed
        :return:
        """

        built_form, built_form_attributes_dict = self.collect_built_form_attributes()

        building_square_feet_dict = built_form_attributes_dict['building_square_feet']

        building_square_feet_dict['building_sqft_industrial_non_warehouse'] = sum([
            float(building_square_feet_dict['building_sqft_manufacturing']),
            float(building_square_feet_dict['building_sqft_construction_utilities'])
        ])

        building_square_feet_dict.pop('building_sqft_manufacturing')
        building_square_feet_dict.pop('building_sqft_construction_utilities')

        building_square_feet_dict['building_sqft_total'] = sum(
            # TODO sometimes value is null. It never should be
            [float(value) for key, value in building_square_feet_dict.items()]
        )

        building_square_feet_dict['building_sqft_detached_single_family'] = sum([
            float(building_square_feet_dict['building_sqft_single_family_large_lot']),
            float(building_square_feet_dict['building_sqft_single_family_small_lot'])
        ])

        flat_row_dicts = dict(
            built_form_attributes_dict['density'].items() +
            built_form_attributes_dict['parcel_acres'].items() +
            built_form_attributes_dict['basic_attributes'].items() +
            building_square_feet_dict.items() +
            built_form_attributes_dict['irrigation'].items()
        )

        for key, value in flat_row_dicts.items():
            setattr(self, key, value)

        self.dwelling_unit_density = sum([self.single_family_large_lot_density,
                                          self.single_family_small_lot_density,
                                          self.attached_single_family_density,
                                          self.multifamily_2_to_4_density,
                                          self.multifamily_5_plus_density])
        self.residential_density = self.residential_density

        self.household_density = self.dwelling_unit_density * (1 - built_form_attributes_dict['residential_attributes']['vacancy_rate'])
        self.population_density = self.household_density * built_form_attributes_dict['residential_attributes']['hh_avg_size']

        self.retail_density = sum([self.restaurant_density, self.retail_services_density, self.accommodation_density,
                                   self.arts_entertainment_density, self.other_services_density])

        self.office_density = sum([self.office_services_density, self.education_services_density,
                                   self.medical_services_density, self.public_admin_density])

        self.industrial_density = sum([self.manufacturing_density, self.wholesale_density,
                                       self.transport_warehouse_density, self.construction_utilities_density])

        self.agricultural_density = sum([self.agriculture_density, self.extraction_density])

        self.employment_density = sum([self.retail_density, self.office_density,
                                       self.industrial_density, self.agricultural_density])

        self.combined_pop_emp_density = self.employment_density + self.population_density

        self.save()
        if self.built_form_type == 'UrbanPlacetype':
            self.run_placetype_metrics()

    def run_placetype_metrics(self):
        """
        calculate the non-core fields of the flat built form
        """

        built_form = BuiltForm.objects.get_subclass(id=self.built_form_id)

        placetype_component_percents = built_form.placetypecomponentpercent_set.all()

        civic_component_percents = placetype_component_percents.filter(
            placetype_component__component_category__name__in=[Keys.BUILDINGTYPE_CIVIC, Keys.INFRASTRUCTURE_UTILITIES])
        self.percent_civic = civic_component_percents.aggregate(Sum('percent'))['percent__sum'] or 0

        park_component_percents = placetype_component_percents.filter(
            placetype_component__component_category__name=Keys.INFRASTRUCTURE_PARK)
        self.percent_parks = park_component_percents.aggregate(Sum('percent'))['percent__sum'] or 0

        street_component_percents = placetype_component_percents.filter(
            placetype_component__component_category__name=Keys.INFRASTRUCTURE_STREET)
        self.percent_streets = street_component_percents.aggregate(Sum('percent'))['percent__sum'] or 0

        residential_component_percents = placetype_component_percents.filter(
            placetype_component__component_category__name__in=Keys.RESIDENTIAL_BUILDINGTYPE_CATEGORIES)
        self.percent_residential = residential_component_percents.aggregate(Sum('percent'))['percent__sum'] or 0

        employment_component_percents = placetype_component_percents.filter(
            placetype_component__component_category__name__in=Keys.EMPLOYMENT_BUILDINGTYPE_CATEGORIES)
        self.percent_employment = employment_component_percents.aggregate(Sum('percent'))['percent__sum'] or 0

        mixed_use_component_percents = placetype_component_percents.filter(
            placetype_component__component_category__name=Keys.BUILDINGTYPE_MIXED_USE)
        self.percent_mixed_use = mixed_use_component_percents.aggregate(Sum('percent'))['percent__sum'] or 0

        #TODO all of these need to be weighted based on other scores
        self.pt_density = self.get_pt_density()
        self.pt_connectivity = self.get_pt_connectivity()
        self.pt_land_use_mix = self.get_pt_land_use_mix()

        self.pt_score = int(round(float(self.pt_density)*0.3 + float(self.pt_connectivity)*0.4 + float(self.pt_land_use_mix)*0.3))

        self.save()
        #self.set_development_characteristics()

    def set_development_characteristics(self):

        non_civic_developable_pct = self.get_developable_percent(includes_civic=False)
        civic_developable_pct = self.get_developable_percent(includes_civic=True)


    #def get_developable_percent(self, includes_civic=True):
    #
    #    percent_utilities = BuiltForm.objects.get(id=self.built_form_id).filter(
    #       placetype_component__component_category__name__in=[Keys.BUILDINGTYPE_CIVIC, Keys.INFRASTRUCTURE_UTILITIES])\
    #                           .aggregate(Sum('percent'))['percent__sum'] or 0
    #
    #    undevelopable = self.percent_parks + self.percent_streets + percent_utilities + (self.percent_civic if not includes_civic else 0)
    #    return 1 - undevelopable
    #
    #def get_jobs_density(self):
    #    pass

    def get_pt_density(self):

        raw_density = self.population_density + self.employment_density

        # Placetype.objects.all().order_by('building_attribute_set__gross_population_density').reverse()[9]
        # .building_attribute_set.gross_population_density
        tenth_largest = 11.6415251701

        # Incidentally, largest = 91.3676228834, in case we wanted to use that instead?

        # Placetype.objects.all().order_by('building_attribute_set__gross_population_density')[0]\
        # .building_attribute_set.gross_population_density
        smallest = 0

        pt_density_weighted = float(raw_density) / (float(tenth_largest) - float(smallest))
        pt_density = pt_density_weighted if pt_density_weighted <= 10 else 10

        return int(round(pt_density))


    def get_pt_connectivity(self):

        raw_connectivity = self.intersection_density

        # These values come from Placetypes.objects.all().aggregate(Max('intersection_density')) and 'Min'
        # Staticly calculated here so that it doesn't have to get recomputed for each placetype

        min_intersections = 10
        max_intersections = 230

        pt_connectivity = (float(raw_connectivity) / (float(max_intersections) - float(min_intersections)))*10

        return int(round(pt_connectivity))

    def get_pt_land_use_mix(self):
        sqft_inst = float(self.building_sqft_public_admin) + float(self.building_sqft_education_services) + float(self.building_sqft_medical_services)
        sqft_residential = float(self.building_sqft_attached_single_family) + float(self.building_sqft_detached_single_family) + float(self.building_sqft_multifamily_5_plus) + float(self.building_sqft_multifamily_2_to_4)
        sqft_retail = float(self.building_sqft_retail_services) + float(self.building_sqft_arts_entertainment) + float(self.building_sqft_other_services)
        sqft_office = float(self.building_sqft_office_services)

        sqft_total = sqft_inst + sqft_residential + sqft_retail + sqft_office

        if sqft_total >= 0.01:
            for sqft in [sqft_inst, sqft_residential, sqft_retail, sqft_office]:
                sqft = sqft if sqft > 0 else 0.01

            percent_inst = sqft_inst/sqft_total
            percent_residential = sqft_residential/sqft_total
            percent_retail = sqft_retail/sqft_total
            percent_office = sqft_office/sqft_total

            industrial_idx = math.log(percent_inst)*percent_inst if percent_inst else 0.0
            residential_idx = math.log(percent_residential)*percent_residential if percent_residential else 0.0
            retail_idx = math.log(percent_retail)*percent_retail if percent_retail else 0.0
            office_idx = math.log(percent_office)*percent_office if percent_office else 0.0

            land_use_mix_index = ((industrial_idx + residential_idx + retail_idx + office_idx) / -math.log(4))*10
            return int(round(land_use_mix_index))
        else:
            return 0


def create_parcel_acres_dict(built_form, uses):
    parcel_acres_dict = defaultdict(float)

    if isinstance(built_form, Building) or isinstance(built_form, BuildingType):
        parcel_acres = 1
    else:
        parcel_acres = sum([
            primary_component.percent for primary_component in built_form.primary_components.all()
            if primary_component.component_category.name not in Keys.INFRASTRUCTURE_TYPES
        ])

    employment_uses = set([Keys.BUILDING_USE_DEFINITION_CATEGORIES[i] for i in Keys.COMMERCIAL_SUBCATEGORIES if i in uses])
    residential_uses = set([Keys.BUILDING_USE_DEFINITION_CATEGORIES[i] for i in Keys.RESIDENTIAL_SUBCATEGORIES if i in uses])

    multifamily_uses = [i for i in [Keys.MULTIFAMILY_2_TO_4, Keys.MULTIFAMILY_5P] if i in uses]
    single_family_residential_uses = [i for i in Keys.DETACHED_RESIDENTIAL + [Keys.ATTACHED_RESIDENTIAL] if i in uses]

    for employment_use in employment_uses:
        parcel_acres_dict['acres_parcel_employment_' + employment_use.lower()] += parcel_acres

    for residential_use in single_family_residential_uses:
        parcel_acres_dict['acres_parcel_residential_' + residential_use.lower().replace(' ', '_')] += parcel_acres

    if multifamily_uses:
        parcel_acres_dict['acres_parcel_residential_multifamily'] += parcel_acres

    # if the buildingtype has a mix of multifamily residential and any kind of employment,
    # add to the Mixed Use parcel acres
    if multifamily_uses and employment_uses:
        parcel_acres_dict['acres_parcel_mixed_use'] += parcel_acres
        # if the buildingtype has any office, add to the mixed with office category
        if Keys.OFFICE_CATEGORY in employment_uses:
            parcel_acres_dict['acres_parcel_mixed_use_with_office'] += parcel_acres
        else:
            parcel_acres_dict['acres_parcel_mixed_use_without_office'] += parcel_acres

    # if the buildingtype has a mix of employment types with no multifamily residential,
    # add to the Mixed Employment parcel acres and to the Employment parcel acres
    if employment_uses and not multifamily_uses:
        parcel_acres_dict['acres_parcel_employment'] += parcel_acres
        if len(employment_uses) > 1:
            parcel_acres_dict['acres_parcel_employment_mixed'] += parcel_acres

    if residential_uses and not employment_uses:
        parcel_acres_dict['acres_parcel_residential'] += parcel_acres

    return parcel_acres_dict
