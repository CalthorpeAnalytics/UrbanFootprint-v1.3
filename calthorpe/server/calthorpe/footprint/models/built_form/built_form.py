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
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com
import glob
import os
import subprocess
from django.db import models
from django.template.defaultfilters import slugify
from model_utils.managers import InheritanceManager
from footprint.mixins.key import Key
from footprint.initialization.fixtures.client.default.built_form.placetype_examples import PLACETYPE_EXAMPLES
from footprint.mixins.building_attributes import BuildingAttributes
from footprint.mixins.key import Key
from footprint.mixins.name import Name
from footprint.mixins.tags import Tags
from footprint.models.presentation.medium import Medium
from footprint.models.presentation.built_form_example import BuiltFormExample
from footprint.utils.utils import timestamp
from footprint.utils.utils import get_or_none
from django.conf import settings

__author__ = 'calthorpe'


class BuiltForm(Name, Key, Tags, BuildingAttributes):
    """
    The base type for :model:`auth.User`, :model:`footprint.built_form.building.Building`, Buildingtypes, Placetypes, Infrastructure and InfrastructureTypes

    """
    objects = InheritanceManager()
    origin_built_form = models.ForeignKey('BuiltForm', null=True)
    medium = models.ForeignKey('Medium', null=True)
    media = models.ManyToManyField(Medium, related_name='built_form_media')
    examples = models.ManyToManyField(BuiltFormExample, null=True)

    BUILT_FORM_IMAGES_DIR = 'builtform_images'

    class Meta(object):
    # This is not abstract so that django can form a many-to-many relationship with it in built_form_set
        abstract = False
        app_label = 'footprint'

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name

    #    def register_component_changes(self):
    #
    #        component_field = self.get_component_field()
    #        if component_field:
    #            m2m_changed.connect(on_collection_modify, sender=component_field.through, weak=False)

    def get_building_attribute_class(self):
        """
        Looks up the child class (Placetype, BuildingType, Building)

        :return: Child class of the built form or None if the BuiltForm is has no Building components
        """
        # this is rough, but it's a way to look up which model the built form is living in (we're only interested in
        # BuildingTypes and PlaceTypes for this release
        from footprint.models import Placetype, PlacetypeComponent, PrimaryComponent

        for clazz in PrimaryComponent, PlacetypeComponent, Placetype:
            built_form = get_or_none(clazz, id=self.id)
            if built_form:
                return built_form
        return None

    def get_component_field(self):
        """
        Returns the ModelField that holds this class's component instances (e.g. placetype_components for the
        PlaceType class)

        :return:
        """
        return None

    def get_components(self, **kwargs):
        """
        Returns the component instances of this class, optionally filtered with the given kwargs. Returns None for
        classes without components (e.g. Buildings)
        :param kwargs: Typical Query parameters used to filter the results

        :return:
        """
        component_field = self.get_component_field()
        if not component_field:
            return None

        return component_field.filter(**kwargs) if len(kwargs) > 0 else component_field.all()

    def custom_aggregation_methods(self):
        pass

    def aggregate_built_form_attributes(self):
        """
        Sums the basic facts of built forms up to their aggregate type.
        :return: None
        """
        pass

    def create_built_form_medium(self, color):
        medium_key = "built_form_{0}".format(self.id)
        medium = update_or_create_built_form_medium(medium_key, color)
        self.medium = medium
        self.save()
        return medium

    def update_or_create_built_form_media(self):

        built_form_key = self.key
        path_root = '%s/footprint/sproutcore/apps/fp/resources/%s' % (settings.PROJECT_ROOT, self.BUILT_FORM_IMAGES_DIR)

        pt_specific_image_folder = '%s/%s' % (path_root, built_form_key)
        default_images_folder = '%s/%s' % (path_root, 'default')

        # Create the BuiltForm's Medium if needed
        # TODO we might want to use a Template here instead. We already create BuiltForm Templates for Feature classes that
        # have BuiltForm styling
        self.media.clear()

        image_paths = glob.glob(pt_specific_image_folder + '/*.*')
        image_directory = built_form_key

        if not image_paths:
            image_paths = glob.glob(default_images_folder + '/*.*')
            image_directory = "default"

        # image_paths = glob.glob(pt_specific_image_folder + '/*.*') if glob.glob(pt_specific_image_folder + '/*.*') else \
        #     glob.glob(default_images_folder + '/*.*')

        # if there are no images in the folder for a particular placetype, use the images in 'default'
        for image_path in image_paths:

            image_name = os.path.basename(image_path)
            image_key = built_form_key + '_' + image_name
            media = Medium.objects.update_or_create(
                key=image_key,
                defaults=dict(url='%s/%s/%s' % (self.BUILT_FORM_IMAGES_DIR, image_directory, image_name))
            )[0]
            self.media.add(media)



    def update_or_create_built_form_examples(self):

        built_form_key = self.key

        self.examples.clear()
        list_of_examples = PLACETYPE_EXAMPLES[built_form_key] if PLACETYPE_EXAMPLES.get(built_form_key) else PLACETYPE_EXAMPLES["default"]


        for object in list_of_examples:

            name = object["example_name"]
            name_slug = slugify(name).replace('-','_')
            url = object["example_url"]
            example = BuiltFormExample.objects.update_or_create(
                key="%s_%s" % (built_form_key, name_slug),
                defaults=dict(
                    url=url,
                    name=name
                ))[0]
            self.examples.add(example)

def update_or_create_built_form_medium(medium_key, color):
    # Create the BuiltForm's Medium if needed
    # TODO we might want to use a Template here instead. We already create BuiltForm Templates for Feature classes that
    # have BuiltForm styling
    medium, created, updated = Medium.objects.update_or_create(
        key=medium_key,
        defaults={
            'content_type': 'color',
            'content': {'fill': {'color': color}, }
        })
    # Set color in case we're doing an update
    medium.content['fill']['color'] = color
    medium.save()
    return medium


def dump_built_forms():
    """
    Exports all of the content of all of the tables that represent BuiltForm to a SQL file that can be most easily
    distributed to other machines and loaded more quickly for tests. Avoids redundantly running the costly calculation
    of the built form relationships.

    :return:
    """
    built_form_tables = [
        "building", "buildingattributes", "buildingpercent", "buildingtype", "buildingtypecategory",
        "buildingusedefinition", "buildingusepercent", "builtform", "builform_tags",
        "builtformset", "builtformset_built_forms", "flatbuiltform", "infrastructure", "infrastructureattributeset",
        "infrastructurepercent", "infrastructuretype", "placetype", "placetypecomponent", "placetypecomponentpercent",
        "medium"
    ]

    formatted_list_of_tables = ""
    for table_name in built_form_tables:
        formatted_list_of_tables += '-t footprint_{table_name} '.format(table_name=table_name)

    dump_args = dict(
        database=settings.DATABASES['default']['NAME'],
        formatted_list_of_tables=formatted_list_of_tables,
        output_file="{sql_path}/built_form_export_{timestamp}.sql".format(
            sql_path=settings.SQL_PATH, timestamp=timestamp()
        ),
        tmp_db_name="urbanfootprint_builtform_dump"
    )

    print dump_args

    dump_command = "pg_dump {database} {formatted_list_of_tables} > {output_file}"

    create_tmp_db = "createdb {tmp_db_name} --template template_postgis"

    restore_dump_to_tmp_db = "psql {tmp_db_name} -f {output_file}"

    delete_unrelated_media = """psql {tmp_db_name} -c "DELETE from footprint_medium
            where \"key\"::text NOT LIKE 'built_form%'"
            """

    delete_dumpfile = "rm {output_file}"

    dump_isolated_built_form_relations = "pg_dump {tmp_db_name} {formatted_list_of_tables} > {output_file}"

    drop_tmp_db = "psql {database} -c \"drop database {tmp_db_name}\""

    for command in [dump_command, create_tmp_db, restore_dump_to_tmp_db, delete_unrelated_media,
                    delete_dumpfile, dump_isolated_built_form_relations, drop_tmp_db]:
        try:
            subprocess.call(command.format(**dump_args), shell=True)
        except Exception, E:
            print E


def resolve_attributes_for_components(sender, **kwargs):
    built_form = kwargs['instance']
    try:
        built_form = built_form.aggregate()
    except Exception, E:
        print Exception, E
    built_form.aggregate_built_form_attributes()


def on_collection_modify(sender, **kwargs):
    resolve_attributes_for_components(sender, **kwargs)