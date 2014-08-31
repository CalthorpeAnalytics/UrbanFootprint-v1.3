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
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from model_utils.managers import InheritanceManager
from django.conf import settings
from footprint.main.mixins.cloneable import Cloneable
from footprint.main.mixins.deletable import Deletable
from footprint.main.mixins.key import Key
from footprint.main.mixins.name import Name
from footprint.main.mixins.tags import Tags
from footprint.main.models.presentation.medium import Medium
from footprint.main.models.presentation.built_form_example import BuiltFormExample
from footprint.main.utils.utils import timestamp, first_or_default
from footprint.main.utils.utils import get_or_none
import logging

logger = logging.getLogger(__name__)


__author__ = 'calthorpe_associates'


class BuiltForm(Name, Key, Tags, Deletable, Cloneable):
    """
    The base type for :model:`auth.User`, :model:`main.built_form.building.Building`, Buildingtypes, Placetypes, Infrastructure and InfrastructureTypes

    """
    objects = InheritanceManager()

    medium = models.ForeignKey('Medium', null=True)
    media = models.ManyToManyField(Medium, related_name='built_form_media')
    examples = models.ManyToManyField(BuiltFormExample, null=True)
    # The user who created the config_entity
    creator = models.ForeignKey(User, null=False, related_name='built_form_creator')
    # The user who last updated the db_entity
    updater = models.ForeignKey(User, null=False, related_name='built_form_updater')

    BUILT_FORM_IMAGES_DIR = 'builtform_images'

    # Flag to turn off post-save publishing when the ConfigEntity is running publishers or when triggered from a child
    # built form updating its aggregates
    # This is class scoped
    no_post_save_publishing = False

    class Meta(object):
    # This is not abstract so that django can form a many-to-many relationship with it in built_form_set
        abstract = False
        app_label = 'main'

    @property
    def subclassed_built_form(self):
        return BuiltForm.resolve_built_form(self)

    @classmethod
    def resolve_built_form_by_id(cls, built_form_id):

        return cls.resolve_built_form(BuiltForm.objects.get(id=built_form_id))

    _subclassed_built_form_lookup = {}

    @classmethod
    def resolve_built_form(cls, built_form):
        """
            Pre Django 1.6 bug-fix. Use this instead of select subclasses do deal with the three tier class hierarchy.
        :param built_form:
        :return:
        """
        subclassed_built_form = cls._subclassed_built_form_lookup.get(built_form.id, None)
        if subclassed_built_form:
            return subclassed_built_form

        second_tier_property = first_or_default(filter(lambda attr: hasattr(built_form, attr),
                                                       ['placetype', 'placetypecomponent', 'primarycomponent']))
        if not second_tier_property:
            raise Exception('BuiltForm subclass cannot be resolved: %s' % built_form)
        second_tier = getattr(built_form, second_tier_property)
        first_tier_property = first_or_default(filter(lambda attr: hasattr(second_tier, attr),
                                                      ['urbanplacetype', 'buildingtype', 'building', 'landscapetype', 'croptype', 'crop']))
        instance = getattr(second_tier, first_tier_property) if first_tier_property else second_tier
        cls._subclassed_built_form_lookup[built_form.id] = instance
        return instance


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
        from footprint.main.models import Placetype, PlacetypeComponent, PrimaryComponent

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

    # def aggregate_built_form_attributes(self):
    #     """
    #     Sums the basic facts of built forms up to their aggregate type.
    #     :return: None
    #     """
    #     pass

    def create_built_form_medium(self, color):
        medium_key = "built_form_{0}".format(self.id)
        medium = update_or_create_built_form_medium(medium_key, color)
        self.medium = medium
        self.save()
        return medium

    def update_or_create_built_form_media(self):

        built_form_key = self.key
        path_root = '%s/sproutcore/apps/fp/resources/%s' % (settings.PROJECT_ROOT, self.BUILT_FORM_IMAGES_DIR)

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

    def update_or_create_built_form_examples(self, array_of_examples):

        built_form_key = self.key

        self.examples.clear()

        for object in array_of_examples:

            name = object["study_area_name"]
            name_slug = slugify(name).replace('-','_')
            study_area_aerial_map_view = object["study_area_aerial_map_view"]
            study_area_street_view = object["study_area_street_view"]
            example = BuiltFormExample.objects.update_or_create(
                key="%s_%s" % (built_form_key, name_slug),
                defaults=dict(
                    url_aerial = study_area_aerial_map_view,
                    url_street = study_area_street_view,
                    name=name
                ))[0]
            self.examples.add(example)

    def get_percent_set(self):
        return None

    def update_or_create_flat_built_form(self):
        from footprint.main.models.built_form.flat_built_form import FlatBuiltForm
        flat_built_form = FlatBuiltForm.objects.update_or_create(built_form_id=self.id)[0]
        flat_built_form.update_attributes()

    def on_instance_modify(self):

        instance_subclass = self.resolve_built_form(self)

        if str(instance_subclass.__class__.__name__) in ['Building']:
            logger.info("Signal: updating building_attributes of [{0}] {1}" .format(self.__class__.__name__, self))
            instance_subclass.building_attribute_set.calculate_derived_fields()
            instance_subclass.update_or_create_flat_built_form()

        elif str(instance_subclass.__class__.__name__) in ['BuildingType', 'UrbanPlacetype']:
            instance_subclass.aggregate_built_form_attributes()
            instance_subclass.update_or_create_flat_built_form()

        if str(instance_subclass.__class__.__name__) in ['Building', 'BuildingType']:
            for parent_built_form in self.get_aggregate_built_forms():
                logger.info("Signal: updating parent objects of [{0}] {1}" .format(self.__class__.__name__, self))

                percent_set = parent_built_form.get_percent_set()

                if percent_set and percent_set.all():
                    subclassed_placetype = parent_built_form.resolve_built_form(parent_built_form)
                    subclassed_placetype.aggregate_built_form_attributes()
                    subclassed_placetype.update_or_create_flat_built_form()

        if str(instance_subclass.__class__.__name__) in ['Crop', 'CropType']:
            for parent_built_form in self.get_aggregate_built_forms():
                logger.info("Signal: updating parent objects of [{0}] {1}" .format(self.__class__.__name__, self))

                percent_set = parent_built_form.get_percent_set()

                if percent_set and percent_set.all():
                    subclassed_placetype = parent_built_form.resolve_built_form(parent_built_form)
                    subclassed_placetype.aggregate_built_form_attributes()

    # Flag to temporarily disable post-save publishing
    # We disable it until all m2m attributes are saved, since post_save usually needs to compute from those attributes
    _no_post_save_publishing = False

    @classmethod
    def pre_save(cls, user_id, **kwargs):
        """
            Disable post-save publishing for BuiltForms when they save.
            We want to do post_save publishing after nested toMany instances save (e.g. PrimaryComponentPercent)
        """
        BuiltForm._no_post_save_publishing = True

    @classmethod
    def post_save(cls, user_id, objects, **kwargs):
        """
            Explicitly resave to kick of post-save publishing
        """
        BuiltForm._no_post_save_publishing = False
        # Save to kick off the post save processing
        for obj in objects:
            obj.save()

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

