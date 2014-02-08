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

# Mixin to ConfigEntityimport logging
import logging
from footprint.lib.functions import merge, remove_keys
from footprint.models.config.db_entity_interest import DbEntityInterest
from footprint.models.config.interest import Interest
from footprint.models.geospatial.db_entity import DbEntity
from footprint.models.database.information_schema import InformationSchema
from footprint.models.keys.keys import Keys
from footprint.utils.dynamic_subclassing import create_table_for_dynamic_class, get_dynamic_model_class
from footprint.utils.inflection import titleize
from footprint.utils.utils import parse_schema_and_table
logger = logging.getLogger(__name__)

class ConfigEntityDbEntitySetup(object):
    def _create_db_entity_and_subclass_with_dynamic_associations(self, **kwargs):
        """
            For dynamic subclasses that have an many-to-many association with a dynamic through class, this creates the
            dynamic through class's table if needed and passes the dynamic through class to a lambda to create the field
            definition.
        :param kwargs:
            'key':Used for the DBEntity key and table name, and also used to name the dynamic subclass of
            kwargs['base_class'] TODO: It might be better to use a seperate name so that the feature class table can
            have the word 'feature' in it instead of 'layer;
             'db_entity_clazz' is optional and indicates the subclass to construct rather than DbEntity
             'base_class': the class to subclass whose instances represent features of the DbEntity.
             'fields': array of additional model fields for the subclass
            'through_class': the base class of the dynamic through class
            'through_class_key': the table name of the dynamic through class
            'association_field_creator': a lambda that expects one argument, the dynamically created through class. The
            labmda must return a dictionary of one key/value. The key is the field name of the associated fielded and
            the value is a ManyToManyField definition that should use the passed in value as the through class
        :return: a dict with a 'db_entity' key pointing to the DbEntity instance and a 'base_class' key pointing to the
        dynamic feature subclass
        """

        field_dict = kwargs['association_field_creator'](self.full_name_of_db_entity_table(kwargs['through_class_key']))

        # Remove the kwargs keys that were used by this method and append field=field_dict, where field_dict is the
        # single key/value pair created by the user's lambda
        new_kwargs = merge(
            remove_keys(kwargs, ['through_class_key', 'through_class', 'association_field_creator']),
            dict(fields=field_dict))
        return_dict = self.create_db_entity_and_subclass(**new_kwargs)

        import models
        through_class = self._dynamic_model_class(
            key=kwargs['through_class_key'],
            base_class=kwargs['through_class'],
            fields=dict(
                feature=models.ForeignKey(
                    # Calculate the name of the feature class since we haven't created it yet
                    return_dict['feature_class']
                )))
        return merge(return_dict, dict(through_class=through_class))

    def create_db_entity_and_subclass(self, **kwargs):
        """
            Returns a dictionary containing a DbEntity instance and a dynamic feature subclass based on the the class
            referenced by kwargs['base_class'] and optionally extra fields referenced by kwargs['fields'].
            The dynamic subclass instances represent features of the layer represented by the DbEntity instance.
        :param kwargs:
         'key':Used for the DBEntity key and table name, and also used to name the dynamic subclass of
            kwargs['base_class'] TODO: It might be better to use a separate name so that the feature class table
            can have the word 'feature' in it instead of 'layer;
         'db_entity_clazz' is optional and indicates the subclass to construct rather than DbEntity
         'base_class': the class to subclass whose instances represent features of the DbEntity.
         'fields': array of additional model fields for the subclass
        :return: a dict with a 'db_entity' key pointing to the DbEntity instance and a 'feature_class' key pointing to
            the dynamic feature subclass that was created based on the base_class and config_entity
        """
        return merge(dict(db_entity=self._update_or_create_db_entity(**kwargs)),
                     {'feature_class': self._dynamic_model_class(**kwargs)},
                     kwargs)

    def create_db_entity(self, **kwargs):
        """
            Updates or creates the DbEntity specified by the kwargs and returns a dict matching the fom of other
            DbEntity setup dicts. Use this when the DbEntity has no accompanying feature_class
        :param kwargs:
         'key':Used for the DBEntity key and table name, and also used to name the dynamic subclass of
            kwargs['base_class'] TODO: It might be better to use a separate name so that the feature class table
            can have the word 'feature' in it instead of 'layer;
         'db_entity_clazz' is optional and indicates the subclass to construct rather than DbEntity
         'url' is optional and indicates the url source of the db_entity (for remote ones)
         'hosts' is optional and indicates and array of host url prefixes for the url
        :return: {'db_entity':the db_entity instance, **kwargs}
        """
        return merge(dict(db_entity=self._update_or_create_db_entity(**kwargs)),
                     kwargs)

    def _update_or_create_db_entity(self, **kwargs):
        """
            Creates a DBEntity in this instance's based on kwargs['key']. The key, name, and table all use the key,
            unless the table or name argument overrides the key. The key will also not name the table is query is
            specified.
        :param kwargs:
         'key' is required and represents the key of the DbEntity instance.
         'name' is optionally used in favor of key for the db_entity name
         'table' is optionally used in place of the key for the table name
         'query' is optionally used to specify a serializable Django query.
         'group_by' is optionally used to specify a default serializable Django aggregate
         'db_entity_clazz' is optional and indicates the subclass to construct rather than DbEntity
         'url' is optional and indicates the url source of the db_entity (for remote ones)
         'hosts' is optional and indicates and array of host url prefixes for the url
        :return: an saved DbEntity
        """
        key = kwargs['key']
        table = kwargs.get('table', kwargs['key'] if not kwargs.get('query', None) else None)
        name = kwargs.get('name', '{0} for {1}'.format(titleize(kwargs['key']), self.name))
        db_entity_clazz = kwargs.get('db_entity_clazz', DbEntity)
        query = kwargs.get('query', None)
        group_by = kwargs.get('group_by', None)
        class_key = kwargs.get('class_key', None)
        url = kwargs.get('url', None)
        hosts = kwargs.get('hosts', None)

        # We distinguish the DbEntity by key, name, and schema. Multiple DbEntities with the same key is a schema
        # may exist, but they must have different names to distinguish them
        return db_entity_clazz.objects.update_or_create(
            key=key,
            schema=self.schema(),
            defaults=dict(
                name=name,
                table=table,
                query=query,
                group_by=group_by,
                class_key=class_key,
                url=url,
                hosts=hosts
            )
        )[0]

    def _dynamic_model_class(self, **kwargs):
        return get_dynamic_model_class(
            kwargs['base_class'],
            self.schema(),
            kwargs['key'],
            #self.full_name_of_db_entity_table(kwargs['key']),
            #class_name=self.class_name_of_db_entity(kwargs['base_class']),
            class_attrs={'config_entity': self, 'override_db': self.db},
            fields=kwargs.get('fields', {}),
            scope=self)

    def sync_db_entities(self, *db_entity_setups):
        """
            Configures saved DbEntities by creating their subclass tables if needed and their DbEntityInterest. This
            is an extension of sync_default_db_entities but is also used by publishers to configure the DbEntities
            that they need that aren't part of the default sets.
            kwargs: 'no_save':True indicates that the config_entity shouldn't be saved explicitly because we are
            already in a post_config_entity save handler
        :return:
        """
        db_entity_interests = []
        for db_entity_setup in db_entity_setups:
            db_entity = db_entity_setup['db_entity']
            # The optional FeatureClass to subclass and for which to create a schema-specific table
            feature_class = db_entity_setup.get('feature_class', None)
            # The optional through-class to subclass and for which to create a schema-specific table
            # The through class is an association class/table between the FeatureClass/table and some other table
            through_class = db_entity_setup.get('through_class', None)

            # Create the DbEntityInterest through class instance which associates the ConfigEntity instance
            # to the DbEntity instance. For now the interest attribute is hard-coded to OWNER. This might
            # be used in the future to indicate other levels of interest
            interest = Interest.objects.get(key=Keys.INTEREST_OWNER)
            db_entity_interest, created, updated = DbEntityInterest.objects.update_or_create(
                config_entity=self,
                db_entity=db_entity,
                interest=interest)
            if created:
                db_entity_interests.append(db_entity_interest)

            if feature_class:

            # Check to see if the FeatureClass table exists in the ConfigEntity's schema. Create it if it doesn't exist
                feature_class_table = feature_class._meta.db_table

                if not InformationSchema.objects.table_exists(*parse_schema_and_table(feature_class_table)):
                    info = "feature class {feature_class} doesn't exist -- creating it \n"
                    logger.info(info.format(feature_class=feature_class_table))
                    create_table_for_dynamic_class(feature_class)
                if through_class:
                    through_class_table = through_class._meta.db_table
                    # Check to see if through class table exists in the ConfigEntity's schema. Create it if it doesn't exist
                    if not InformationSchema.objects.table_exists(*parse_schema_and_table(through_class_table)):
                        info = "through class {through_class} or {feature_class} doesn't exist -- creating it \n"
                        logger.info(info.format(through_class=through_class_table, feature_class=feature_class.name))
                        create_table_for_dynamic_class(through_class)

        # Do a forced adoption of DbEntityInterests from the parent ConfigEntity. This makes sure that ConfigEntity has
        # the parent's DbEntityInterests before adding any of its own. Otherwise the parent's are never adopted.
        # See _adopt_from_donor docs for an explanation.
        self._adopt_from_donor('db_entities', True)
        # Now add the db_entity_interests that were created
        self.add_db_entity_interests(*db_entity_interests)

