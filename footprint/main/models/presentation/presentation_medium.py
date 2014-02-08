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
from django.db import models
from model_utils.managers import InheritanceManager
from picklefield import PickledObjectField
from footprint.main.mixins.deletable import Deletable
from medium import Medium
from footprint.main.mixins.tags import Tags

__author__ = 'calthorpe_associates'

class PresentationMedium(Tags, Deletable):
    """
        Links media to a PresentationConfig and also links the medium to a db_entity of the presentation_config via
        StyleConfig instances
    """
    objects = InheritanceManager()
    #objects = CustomQuerySet.as_manager()

    presentation = models.ForeignKey('Presentation')
    medium = models.ForeignKey(Medium)

    # Used to indicate whether the instance is currently visible in the presentation. This is useful for a layers
    # on a map, charts, etc., when some need to be hidden
    visible = models.BooleanField(default=True)
    visible_attributes = PickledObjectField(null=True)

    # An optional key reference to a DbEntry known by the presentation's config_entity via a DbEntityInterest.
    # The referenced DbEntity indicates the this instance is associated with DbEntity. For example, if the
    # DbEntity is a geographic table, the medium might be the Style medium that decorates that table as a visible Layer.
    # Multiple media and thus PresentationMedia instance may have the same db_entity_key.
    # The reason this is used instead of the db_entity ForeignKey so this instance doesn't have to keep up with the
    # currently selected DbEntity. Use db_entity() to resolve the selected DbEntity
    db_entity_key = models.CharField(max_length=50, null=False, blank=False)

    # When them medium is a Template that requires context dict of wildcard values to produce a complete medium,
    # the currently context dict is stored here. It's initial value should be set to medium.template_context.context,
    # which is the default context.
    # Example: medium = Template(template_context=TemplateContext(context=dict(foo='red', bar='blue')) then
    # medium.medium_context would initially equal dict(foo='red', bar='blue') but could subsequently be updated by
    # a user to be dict(foo='purple', bar='aqua')
    # The dict might be more complex and be keyed by db_entity table attributes in order to style individual attributes
    medium_context = PickledObjectField(null=True)

    # Optional configuration meant for non-stylistic or medium related value. For instance, a result graph might store
    # it's axis labels and axis increments here
    configuration = PickledObjectField(null=True)

    # Optional. When medium is a Template this combines renders the medium.content as a template with medium_context as
    # its context. The rendered_medium can take any form. It might be a dict keyed by DbEntity column names and valued
    # by CSS, for instance
    rendered_medium = PickledObjectField(null=True)

    @property
    def db_entity_interest(self):
        """
            Returns the ConfigEntity's selected DbEntityInterest of the key self.db_entity_key.
            This will be None when a new layer is created that doesn't have an associated
            DbEntity instance yet. This case will disappear as soon as we start saving
            the new DbEntity before the new Layer.
        :return:
        """
        return self._db_entity_interest or \
            self.presentation.subclassed_config_entity.computed_db_entity_interests(db_entity__key=self.db_entity_key)[0]

    # We accept a db_entity_interest to allow the PresentationMediumResource to save new
    # DbEntityInterests. After saving this field is set back to None
    _db_entity_interest = None
    @db_entity_interest.setter
    def db_entity_interest(self, value):
        self._db_entity_interest = value
    def save(self, force_insert=False, force_update=False, using=None):
        # Clear this. We'll access it from the config_entity after initial save
        self._db_entity_interest = None
        super(PresentationMedium, self).save(force_insert, force_update, using)

    def __unicode__(self):
        return "presentation: {0}, medium: {1}".format(unicode(self.presentation), unicode(self.medium))

    def query(self):
        return self.get_data()

    def get_data(self, **kwargs):
        """
            Return the DbEntity data of the PresentationMedium in cases where DbEntities are modeled by a feature class.
            The feature class of the config_entity, db_entity combination will either return all results or return
            the query defined on the db_entity, if there is one. Optionally provide a group_by clause (see DbEntity for
            syntax)
            :param kwargs['group_by'] overrides or provides the DbEntity query with a group by--aggregating values and determining
            what fields are returned. This will make the return data always a list of dicts.
            :param kwargs['values'] overrides or provides the DbEntity query with
        :return:
        """
        return self.db_entity_interest.db_entity.run_query(self.presentation.subclassed_config_entity, **kwargs)

    def save(self, force_insert=False, force_update=False, using=None):
        super(PresentationMedium, self).save(force_insert, force_update, using)
        self.update_tags()

    def update_tags(self):
        """
            Optionally updates an instance's tags. Overridden by the subclass
        """
        pass

    class Meta(object):
        app_label = 'main'
        verbose_name_plural = 'presentation_media'

