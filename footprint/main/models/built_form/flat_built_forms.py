# coding=utf-8
import csv
import math
import logging
from collections import defaultdict
from django.db.models import Sum
from django.template.defaultfilters import slugify
from footprint.main.models.built_form.built_form import BuiltForm
from footprint.main.models.built_form.placetype_component import PlacetypeComponent
from footprint.main.models.built_form.primary_component import PrimaryComponent
from footprint.main.models.built_form.placetype import Placetype
from footprint.main.models.keys.keys import Keys

from django.conf import settings

__author__ = 'calthorpe_associates'

from django.db import models
logger = logging.getLogger(__name__)


class FlatBuiltForm(models.Model):
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
        built_form = BuiltForm.objects.get_subclass(id=self.built_form_id)

        type = built_form.__class__.__name__
        key_prepend = 'b__' if type == 'PrimaryComponent' else 'bt__' if type == "PlacetypeComponent" else "pt__"
        attributes = built_form.building_attributes
        if not attributes:
            raise Exception("No attributes for " + built_form)
        built_form_dict = {
            'basic_attributes': {
                'name': built_form.name,
                'key': key_prepend + slugify(built_form.name).replace('-', '_'),
                'built_form_type': type,
                'gross_net_ratio': attributes.gross_net_ratio,
                'household_density': attributes.household_density,
                'population_density': attributes.gross_population_density,
                'intersection_density': built_form.intersection_density if isinstance(built_form, Placetype) else 0
            },
            'density': defaultdict(float),
            'parcel_acres': defaultdict(float),
            'building_square_feet': defaultdict(float),
            'irrigation': defaultdict(float)
        }

        # do parcel acres first
        if built_form.__class__ in [PlacetypeComponent, PrimaryComponent]:
            uses = list(attributes.buildingusepercent_set.all().values_list(
                'building_use_definition__name', flat=True))
            built_form_dict['parcel_acres'] = create_parcel_acres_dict(built_form, uses)

        if built_form.__class__ == Placetype:

            parcel_acres_dict = defaultdict(float)

            for component_percent in built_form.placetypecomponentpercent_set.filter():
                component = component_percent.component()
                uses = component.building_attributes.buildingusepercent_set.all()
                use_names = list(uses.values_list('building_use_definition__name', flat=True))
                component_parcel_acres_dict = create_parcel_acres_dict(component, use_names)

                for key, value in component_parcel_acres_dict.items():
                    parcel_acres_dict[key] += value * float(component_percent.percent)

            built_form_dict['parcel_acres'] = parcel_acres_dict

        for use in attributes.buildingusepercent_set.all():
            use_name = use.building_use_definition.name.lower().replace(' ', '_')
            built_form_dict['building_square_feet']['building_sqft_' + use_name] = use.gross_built_up_area
            built_form_dict['density'][use_name + "_density"] = use.unit_density

        irrigation_dict = built_form_dict['irrigation']

        irrigation_dict['softscape_and_landscape_percent'] = attributes.softscape_and_landscape_percent
        irrigation_dict['irrigated_percent'] = attributes.irrigated_percent

        irrigation_dict['residential_irrigated_square_feet'] = attributes.residential_irrigated_square_feet or 0
        irrigation_dict['commercial_irrigated_square_feet'] = attributes.commercial_irrigated_square_feet or 0

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
            [float(value or 0) for key, value in building_square_feet_dict.items()]
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
            # self.save()

        # TODO some of these values are null and never should be
        self.attached_single_family_density = self.attached_single_family_density or 0
        self.building_sqft_attached_single_family = self.building_sqft_attached_single_family or 0
        self.dwelling_unit_density = sum([self.single_family_large_lot_density or 0,
                                          self.single_family_small_lot_density or 0,
                                          self.attached_single_family_density,
                                          self.multifamily_2_to_4_density or 0,
                                          self.multifamily_5_plus_density or 0])

        self.employment_density = sum([self.retail_density, self.office_density,
                                       self.industrial_density, self.agricultural_density])

        if self.built_form_type == 'Placetype':
            self.run_placetype_metrics()
        self.save()

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

        # Placetype.objects.all().order_by('building_attributes__gross_population_density').reverse()[9]
        # .building_attributes.gross_population_density
        tenth_largest = 11.6415251701

        # Incidentally, largest = 91.3676228834, in case we wanted to use that instead?

        # Placetype.objects.all().order_by('building_attributes__gross_population_density')[0]\
        # .building_attributes.gross_population_density
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


def refresh_all_flat_built_forms():
    """
    clears the set of flat built forms and pulls the information over again
    :return:
    """
    FlatBuiltForm.objects.all().delete()
    logger.info("exporting {0} placetypes, {1} buildingtypes, and {2} buildings".format(len(Placetype.objects.all()),
                                                                                  len(PlacetypeComponent.objects.all()),
                                                                                  len(PrimaryComponent.objects.all())))

    for built_form in BuiltForm.objects.all().select_subclasses():
        if built_form.__class__ in [Placetype, PlacetypeComponent, PrimaryComponent]:
            FlatBuiltForm(built_form_id=built_form.id).save()
    for fbf in FlatBuiltForm.objects.all():
        fbf.update_attributes()

    # # Read in placetype descriptions and create a dictionary so you
    descriptions_file = '%s/sproutcore/apps/fp/resources/Text/%s' % (settings.PROJECT_ROOT, 'placetype_descriptions.csv')
    reader = csv.reader(open(descriptions_file, 'r'))
    descriptions = {}

    for row in reader:
        if row:
            k,v = row
            descriptions[k] = v

    for fbf in FlatBuiltForm.objects.all():
        fbf.description = descriptions[fbf.key] if descriptions.get(fbf.key) else "No description available"
        fbf.save()

    bf_additional_attr_file = 'Place_Type_Additional_Attributes_Oct_31_2013.csv'
    # # Read in placetype examples and create a dictionary so you
    bf_additional_attr_path = '%s/sproutcore/apps/fp/resources/Text/%s' % (settings.PROJECT_ROOT, bf_additional_attr_file)
    reader = csv.DictReader(open(bf_additional_attr_path, "rU"))

    #This dictionary has builtform id's as the key, and the value is another dictionary with various extra data
    bf_additional_attr = {}

    for row in reader:
        if row:
            key = row["pt__key"]
            bf_additional_attr[key] = row

    for fbf in FlatBuiltForm.objects.all():
        #Come back here and either add the name or the so it accesses dict b
        if bf_additional_attr.get(fbf.key):

            fbf.intersections_sqmi = int(float(bf_additional_attr[fbf.key]["intersections_sqmi"]))
            fbf.block_avg_size_acres = float(bf_additional_attr[fbf.key]["block_avg_size_acres"])
            fbf.street_pattern = bf_additional_attr[fbf.key]["street_pattern"]
            fbf.avg_estimated_building_height_feet = int(float(bf_additional_attr[fbf.key]["avg_estimated_building_height_feet"]))
            fbf.building_avg_number_of_floors = int(float(bf_additional_attr[fbf.key]["building_avg_number_of_Floors"]))

            fbf.save()


def create_parcel_acres_dict(built_form, uses):
    parcel_acres_dict = defaultdict(float)

    if isinstance(built_form, PrimaryComponent) or isinstance(built_form, PlacetypeComponent):
        parcel_acres = 1
    else:
        parcel_acres = sum([
            primary_component.percent for primary_component in built_form.primary_components.all()
            if primary_component.component_category.name not in Keys.INFRASTRUCTURE_TYPES
        ])

    employment_uses = [i for i in ['Office', 'Retail', 'Industrial', 'Agricultural'] if i in uses]
    multifamily_uses = [i for i in [Keys.MULTIFAMILY_2_TO_4, Keys.MULTIFAMILY_5P] if i in uses]

    for base_use in ('Retail', 'Industrial', 'Office', 'Agricultural'):
        if base_use in uses:
            parcel_acres_dict['acres_parcel_employment_' + base_use.lower()] += parcel_acres

    # TODO : acres parcel single_family_residential isn't getting values
    single_family_residential_uses = Keys.DETACHED_RESIDENTIAL + [Keys.ATTACHED_RESIDENTIAL]
    for residential_use in single_family_residential_uses:
        if residential_use in uses:
            parcel_acres_dict['acres_parcel_residential_' + residential_use.lower().replace(' ', '_')] += parcel_acres

    if multifamily_uses:
        parcel_acres_dict['acres_parcel_residential_multifamily'] += parcel_acres

    # if the buildingtype has a mix of multifamily residential and any kind of employment,
    # add to the Mixed Use parcel acres
    if multifamily_uses and employment_uses:
        parcel_acres_dict['acres_parcel_mixed_use'] += parcel_acres
        # if the buildingtype has any office, add to the mixed with office category
        if 'Office' in employment_uses:
            parcel_acres_dict['acres_parcel_mixed_use_with_office'] += parcel_acres
        else:
            parcel_acres_dict['acres_parcel_mixed_use_without_office'] += parcel_acres

    # if the buildingtype has a mix of employment types with no multifamily residential,
    # add to the Mixed Employment parcel acres and to the Employment parcel acres
    if employment_uses and not multifamily_uses:
        parcel_acres_dict['acres_parcel_employment'] += parcel_acres
        if len(employment_uses) > 1:
            parcel_acres_dict['acres_parcel_employment_mixed'] += parcel_acres

    if 'Residential' in uses and not employment_uses:
        parcel_acres_dict['acres_parcel_residential'] += parcel_acres

    return parcel_acres_dict
