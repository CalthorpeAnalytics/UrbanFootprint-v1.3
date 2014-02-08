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
import itertools
import csv

from django.db.models.signals import post_save
from django.template.defaultfilters import slugify

from footprint.main.initialization.built_form.built_form_importer import BuiltFormImporter
from footprint.client.configuration.default.default_mixin import DefaultMixin
from footprint.main.lib.functions import map_to_dict
from footprint.main.models import BuildingUsePercent, PlacetypeComponentPercent, PrimaryComponent, \
    PrimaryComponentPercent, Placetype, BuildingAttributeSet, PlacetypeComponent, GlobalConfig
from footprint.client.configuration.fixture import BuiltFormFixture
from footprint.main.models.built_form.placetype_component import PlacetypeComponentCategory
from footprint.main.models.tag import Tag
from footprint.main.tests.test_data.sample_built_form_sets import load_placetype_csv
from footprint import settings
from django.conf import settings


__author__ = 'calthorpe'

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

# By default we create a BuiltFormSet for each class, one for Placetypes, BuildingTypes, and Buildings.
# Sets can contain instances of multiple classes, but this is the configuration is easiest to understand
class DefaultBuiltFormFixture(DefaultMixin, BuiltFormFixture):

    def update_or_create_building_attributes(self, built_form, building_attributes_dict, built_form_created):
        if built_form_created:
            building_attributes = BuildingAttributeSet.objects.create(**building_attributes_dict)
            built_form.building_attributes = building_attributes
            built_form.save()
        else:
            building_attributes = built_form.building_attributes
            for (key, value) in building_attributes_dict.items():
                setattr(building_attributes, key, value)
            built_form.save()

    def built_forms(self, client='default'):
        """
            Returns an unpersisted dict with lists placetypes, buildingtypes, buildings, etc. fixtures
        :param default_built_forms:
        :return:
        """

        # Create the definitions for all default built_forms in the system. These depend on one another and are
        # made into actual instances in persist_built_forms
        if not isinstance(self.config_entity, GlobalConfig) or settings.SKIP_ALL_BUILT_FORMS:
            return {
                'placetypes': [],
                'placeptype_components': [],
                'primary_components': [],
                'primary_component_percents': [],
                'placetype_component_percents': [],
                'building_use_percents': [],
            }

        built_forms_dict = BuiltFormImporter().construct_built_forms(client)
        built_forms = []

        from footprint.main.models.built_form.primary_component import on_instance_modify as on_primary_component_modify

        post_save.disconnect(on_primary_component_modify, sender=PrimaryComponent)
        logger.info("Beginning Primary Components")
        for primary_component_dict in built_forms_dict['primary_components']:
            name = primary_component_dict['building_attributes'].pop('name', None)
            primary_component, created, updated = PrimaryComponent.objects.update_or_create(
                key='b__' + slugify(name).replace('-', '_'),
                defaults=dict(
                    name=name,
                )
            )
            self.update_or_create_building_attributes(primary_component, primary_component_dict['building_attributes'], created)

            built_forms.append(primary_component)

        logger.info("Beginning Building Use Percents")
        for building_use_percent_dict in built_forms_dict['building_use_percents']:
            built_form = PrimaryComponent.objects.get(name=building_use_percent_dict['built_form_name'])
            use_attributes = building_use_percent_dict['built_form_uses']
            definition = use_attributes.pop('building_use_definition')
            use_percent, created, updated = BuildingUsePercent.objects.update_or_create(
                building_attributes=built_form.building_attributes,
                building_use_definition=definition,
                defaults=use_attributes
            )
            pass

        if not settings.TEST_SKIP_BUILT_FORM_COMPUTATIONS:
            logger.info("Calculating Primary Components")
        for primary_component in PrimaryComponent.objects.all():
            if not settings.TEST_SKIP_BUILT_FORM_COMPUTATIONS:
                primary_component.building_attributes.calculate_derived_fields()
        post_save.connect(on_primary_component_modify, sender=PrimaryComponent)

        from footprint.main.models.built_form.placetype_component import on_instance_modify as on_placetype_component_modify

        post_save.disconnect(on_placetype_component_modify, sender=PlacetypeComponent)

        logger.info("Beginning Placetype Components")
        for placetype_component_dict in built_forms_dict['placetype_components']:
            name = placetype_component_dict['name']
            category = placetype_component_dict['component_category']
            color = placetype_component_dict.get('color', "#909090")
            component_category = PlacetypeComponentCategory.objects.get_or_create(name=category)[0]
            placetype_component, created, updated = PlacetypeComponent.objects.update_or_create(
                key='bt__' + slugify(name).replace('-', '_'),
                defaults=dict(
                    name=name,
                    component_category=component_category
                )
            )
            self.update_or_create_building_attributes(placetype_component, {}, created)

            placetype_component.create_built_form_medium(color)

            placetype_component.save()
            built_forms.append(placetype_component)

        logger.info("Beginning Primary Component Percents")
        for primary_component_percent in built_forms_dict['primary_component_percents']:

            placetype_component_dict = PlacetypeComponent.objects.get(
                name=primary_component_percent['placetype_component_name'])
            if primary_component_percent['percent'] > 0:
                PrimaryComponentPercent.objects.update_or_create(
                    primary_component=PrimaryComponent.objects.get(
                        name=primary_component_percent['primary_component_name']
                    ),
                    placetype_component=placetype_component_dict,
                    defaults=dict(percent=primary_component_percent['percent'])
                )
            if not settings.TEST_SKIP_BUILT_FORM_COMPUTATIONS:
                placetype_component_dict.aggregate_built_form_attributes()

        placetype_color_lookup = map_to_dict(
            lambda placetype: [
                placetype.name,
                placetype.color],
            load_placetype_csv())

        examples_file = 'placetype_example_areas.csv'
        # # Read in placetype examples and create a dictionary so you
        bf_examples_path = '%s/sproutcore/apps/fp/resources/Text/%s' % (settings.PROJECT_ROOT, examples_file)
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


        logger.info("Beginning Placetypes")
        for placetype_dict in built_forms_dict['placetypes']:
            name = placetype_dict['building_attributes'].pop('name', None)

            placetype, created, updated = Placetype.objects.update_or_create(
                key='pt__' + slugify(name).replace('-', '_'),
                defaults=dict(
                    name=name,
                    intersection_density=placetype_dict['intersection_density'])
            )
            building_attributes_dict = placetype_dict['building_attributes']
            self.update_or_create_building_attributes(placetype, building_attributes_dict, created)
            placetype.create_built_form_medium(placetype_color_lookup.get(placetype.name, "#909090"))
            placetype.update_or_create_built_form_media()
            placetype.update_or_create_built_form_examples(bf_examples.get(placetype.key) if bf_examples.get(placetype.key) else [])

            built_forms.append(placetype)

            placetype.save()

            placetype_dict = built_forms_dict['placetype_component_percents'].get(placetype.name, None)
            if not placetype_dict:
                logger.warning("Expected built_forms_dict['placetype_component_percents'] to have key %s",
                               placetype.name)
            else:
                for placetype_component_dict, attributes in placetype_dict.items():
                    component = PlacetypeComponent.objects.get(name=placetype_component_dict)
                    if attributes['percent'] > 0:
                        PlacetypeComponentPercent.objects.update_or_create(
                            placetype=placetype,
                            placetype_component=component,
                            defaults=dict(percent=attributes['percent']))

        post_save.connect(on_placetype_component_modify, sender=PlacetypeComponent)

        if not settings.TEST_SKIP_BUILT_FORM_COMPUTATIONS:
            logger.info("Computing Placetypes")
            for placetype in Placetype.objects.all():
                placetype.aggregate_built_form_attributes()

        built_forms_dict = {
            'placetypes': Placetype.objects.all(),
            'placetype_components': PlacetypeComponent.objects.all(),
            'primary_components': PrimaryComponent.objects.all(),

            'primary_component_percents': PrimaryComponentPercent.objects.all(),
            'building_use_percents': BuildingUsePercent.objects.all(),
            'placetype_component_percents': PlacetypeComponentPercent.objects.all()
        }

        return built_forms_dict

    def tag_built_forms(self, built_forms_dict, client='default'):
        """
            Tag BuiltForms based on their character
        :return:
        """
        if settings.SKIP_ALL_BUILT_FORMS:
            return

        built_form_importer = BuiltFormImporter()

        for placetype_component in built_forms_dict.get('placetype_components', []):
            placetype_component.tags.add(
                Tag.objects.update_or_create(tag=placetype_component.component_category.name)[0])

        for built_form in itertools.chain(built_forms_dict.get('placetypes', []),
                                          built_forms_dict.get('primary_components', [])):
            tag, created, updated = Tag.objects.update_or_create(tag='Unsorted')
            if len(built_form.tags.filter(tag=tag.tag)) == 0:
                built_form.tags.add(tag)

    def built_form_sets(self):
        return self.matching_scope([
            dict(
                scope=GlobalConfig,
                key='uf_placetype',
                name='UF Placetypes',
                description='BuiltFormSet containing only placetypes',
                clazz=Placetype,
                client='default'
            ),
            dict(
                scope=GlobalConfig,
                key='uf_placetype_components',
                name='UF BuildingTypes',
                description='BuiltFormSet containing only buildingtypes',
                clazz=PlacetypeComponent,
                client='default'
            ),
            dict(
                scope=GlobalConfig,
                key='uf_primary_components',
                name='Buildings',
                description='BuiltFormSet containing only buildings',
                clazz=PrimaryComponent,
                client='default'
            )
        ], class_scope=self.config_entity and self.config_entity.__class__)
