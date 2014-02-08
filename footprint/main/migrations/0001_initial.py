# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BuildingUsePercent'
        db.create_table('main_buildingusepercent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percent', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=21, decimal_places=20)),
            ('building_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.BuildingAttributeSet'])),
            ('building_use_definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.BuildingUseDefinition'])),
            ('vacancy_rate', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=4, decimal_places=3)),
            ('household_size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3)),
            ('efficiency', self.gf('django.db.models.fields.DecimalField')(default=0.85, max_digits=6, decimal_places=4)),
            ('square_feet_per_unit', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=3)),
            ('floor_area_ratio', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=10)),
            ('unit_density', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10)),
            ('gross_built_up_area', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=13, decimal_places=3)),
            ('net_built_up_area', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=13, decimal_places=3)),
        ))
        db.send_create_signal('main', ['BuildingUsePercent'])

        # Adding model 'BuildingUseDefinition'
        db.create_table('main_buildingusedefinition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.BuildingUseDefinition'], null=True)),
        ))
        db.send_create_signal('main', ['BuildingUseDefinition'])

        # Adding model 'BuildingAttributeSet'
        db.create_table('main_buildingattributeset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parking_spaces', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=7, decimal_places=3)),
            ('parking_structure_square_feet', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('floors', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=3)),
            ('total_far', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=7)),
            ('gross_population_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=10)),
            ('household_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=10)),
            ('impervious_roof_percent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3)),
            ('impervious_hardscape_percent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3)),
            ('pervious_hardscape_percent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3)),
            ('softscape_and_landscape_percent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3)),
            ('irrigated_percent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3)),
            ('hardscape_percent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3)),
            ('residential_irrigated_square_feet', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=2)),
            ('commercial_irrigated_square_feet', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=2)),
            ('residential_average_lot_size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=2)),
            ('gross_net_ratio', self.gf('django.db.models.fields.DecimalField')(default=1, max_digits=8, decimal_places=7)),
            ('combined_pop_emp_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=4)),
        ))
        db.send_create_signal('main', ['BuildingAttributeSet'])

        # Adding model 'Tag'
        db.create_table('main_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('main', ['Tag'])

        # Adding model 'Medium'
        db.create_table('main_medium', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('content', self.gf('picklefield.fields.PickledObjectField')(null=True)),
        ))
        db.send_create_signal('main', ['Medium'])

        # Adding model 'BuiltFormExample'
        db.create_table('main_builtformexample', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('url_aerial', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('url_street', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('content', self.gf('picklefield.fields.PickledObjectField')(null=True)),
        ))
        db.send_create_signal('main', ['BuiltFormExample'])

        # Adding model 'BuiltForm'
        db.create_table('main_builtform', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('building_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.BuildingAttributeSet'], null=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('origin_built_form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.BuiltForm'], null=True)),
            ('medium', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Medium'], null=True)),
        ))
        db.send_create_signal('main', ['BuiltForm'])

        # Adding M2M table for field tags on 'BuiltForm'
        db.create_table('main_builtform_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('builtform', models.ForeignKey(orm['main.builtform'], null=False)),
            ('tag', models.ForeignKey(orm['main.tag'], null=False))
        ))
        db.create_unique('main_builtform_tags', ['builtform_id', 'tag_id'])

        # Adding M2M table for field media on 'BuiltForm'
        db.create_table('main_builtform_media', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('builtform', models.ForeignKey(orm['main.builtform'], null=False)),
            ('medium', models.ForeignKey(orm['main.medium'], null=False))
        ))
        db.create_unique('main_builtform_media', ['builtform_id', 'medium_id'])

        # Adding M2M table for field examples on 'BuiltForm'
        db.create_table('main_builtform_examples', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('builtform', models.ForeignKey(orm['main.builtform'], null=False)),
            ('builtformexample', models.ForeignKey(orm['main.builtformexample'], null=False))
        ))
        db.create_unique('main_builtform_examples', ['builtform_id', 'builtformexample_id'])

        # Adding model 'DbEntity'
        db.create_table('main_dbentity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('schema', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('table', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('srid', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='db_entity_creator', null=True, to=orm['auth.User'])),
            ('updater', self.gf('django.db.models.fields.related.ForeignKey')(related_name='db_entity_updater', null=True, to=orm['auth.User'])),
            ('feature_class_configuration', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('extent_authority', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
            ('hosts', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('query', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('class_key', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('group_by', self.gf('picklefield.fields.PickledObjectField')(null=True)),
        ))
        db.send_create_signal('main', ['DbEntity'])

        # Adding M2M table for field tags on 'DbEntity'
        db.create_table('main_dbentity_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dbentity', models.ForeignKey(orm['main.dbentity'], null=False)),
            ('tag', models.ForeignKey(orm['main.tag'], null=False))
        ))
        db.create_unique('main_dbentity_tags', ['dbentity_id', 'tag_id'])

        # Adding model 'Category'
        db.create_table('main_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('main', ['Category'])

        # Adding model 'BuiltFormSet'
        db.create_table('main_builtformset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
        ))
        db.send_create_signal('main', ['BuiltFormSet'])

        # Adding M2M table for field built_forms on 'BuiltFormSet'
        db.create_table('main_builtformset_built_forms', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('builtformset', models.ForeignKey(orm['main.builtformset'], null=False)),
            ('builtform', models.ForeignKey(orm['main.builtform'], null=False))
        ))
        db.create_unique('main_builtformset_built_forms', ['builtformset_id', 'builtform_id'])

        # Adding model 'Policy'
        db.create_table('main_policy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('schema', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('values', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('main', ['Policy'])

        # Adding M2M table for field tags on 'Policy'
        db.create_table('main_policy_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('policy', models.ForeignKey(orm['main.policy'], null=False)),
            ('tag', models.ForeignKey(orm['main.tag'], null=False))
        ))
        db.create_unique('main_policy_tags', ['policy_id', 'tag_id'])

        # Adding M2M table for field policies on 'Policy'
        db.create_table('main_policy_policies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_policy', models.ForeignKey(orm['main.policy'], null=False)),
            ('to_policy', models.ForeignKey(orm['main.policy'], null=False))
        ))
        db.create_unique('main_policy_policies', ['from_policy_id', 'to_policy_id'])

        # Adding model 'PolicySet'
        db.create_table('main_policyset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
        ))
        db.send_create_signal('main', ['PolicySet'])

        # Adding M2M table for field policies on 'PolicySet'
        db.create_table('main_policyset_policies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('policyset', models.ForeignKey(orm['main.policyset'], null=False)),
            ('policy', models.ForeignKey(orm['main.policy'], null=False))
        ))
        db.create_unique('main_policyset_policies', ['policyset_id', 'policy_id'])

        # Adding model 'ConfigEntity'
        db.create_table('main_configentity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('scope', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('bounds', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='config_entity_creator', null=True, to=orm['auth.User'])),
            ('updater', self.gf('django.db.models.fields.related.ForeignKey')(related_name='config_entity_updater', null=True, to=orm['auth.User'])),
            ('parent_config_entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent_set', null=True, to=orm['main.ConfigEntity'])),
            ('origin_config_entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='clone_set', null=True, to=orm['main.ConfigEntity'])),
            ('selections', self.gf('footprint.main.models.config.model_pickled_object_field.SelectionModelsPickledObjectField')(default={'db_entities': {}, 'sets': {}})),
        ))
        db.send_create_signal('main', ['ConfigEntity'])

        # Adding M2M table for field categories on 'ConfigEntity'
        db.create_table('main_configentity_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('configentity', models.ForeignKey(orm['main.configentity'], null=False)),
            ('category', models.ForeignKey(orm['main.category'], null=False))
        ))
        db.create_unique('main_configentity_categories', ['configentity_id', 'category_id'])

        # Adding M2M table for field built_form_sets on 'ConfigEntity'
        db.create_table('main_configentity_built_form_sets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('configentity', models.ForeignKey(orm['main.configentity'], null=False)),
            ('builtformset', models.ForeignKey(orm['main.builtformset'], null=False))
        ))
        db.create_unique('main_configentity_built_form_sets', ['configentity_id', 'builtformset_id'])

        # Adding M2M table for field policy_sets on 'ConfigEntity'
        db.create_table('main_configentity_policy_sets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('configentity', models.ForeignKey(orm['main.configentity'], null=False)),
            ('policyset', models.ForeignKey(orm['main.policyset'], null=False))
        ))
        db.create_unique('main_configentity_policy_sets', ['configentity_id', 'policyset_id'])

        # Adding M2M table for field media on 'ConfigEntity'
        db.create_table('main_configentity_media', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('configentity', models.ForeignKey(orm['main.configentity'], null=False)),
            ('medium', models.ForeignKey(orm['main.medium'], null=False))
        ))
        db.create_unique('main_configentity_media', ['configentity_id', 'medium_id'])

        # Adding model 'Job'
        db.create_table('main_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hashid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36)),
            ('task_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jobs', to=orm['auth.User'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('status', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ended_on', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('data', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('main', ['Job'])

        # Adding model 'PresentationMedium'
        db.create_table('main_presentationmedium', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('presentation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Presentation'])),
            ('medium', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Medium'])),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('visible_attributes', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('db_entity_key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('medium_context', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('configuration', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('rendered_medium', self.gf('picklefield.fields.PickledObjectField')(null=True)),
        ))
        db.send_create_signal('main', ['PresentationMedium'])

        # Adding M2M table for field tags on 'PresentationMedium'
        db.create_table('main_presentationmedium_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('presentationmedium', models.ForeignKey(orm['main.presentationmedium'], null=False)),
            ('tag', models.ForeignKey(orm['main.tag'], null=False))
        ))
        db.create_unique('main_presentationmedium_tags', ['presentationmedium_id', 'tag_id'])

        # Adding model 'Layer'
        db.create_table('main_layer', (
            ('presentationmedium_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.PresentationMedium'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('main', ['Layer'])

        # Adding model 'PrimaryComponent'
        db.create_table('main_primarycomponent', (
            ('builtform_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.BuiltForm'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('main', ['PrimaryComponent'])

        # Adding model 'PlacetypeComponentCategory'
        db.create_table('main_placetypecomponentcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contributes_to_net', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('main', ['PlacetypeComponentCategory'])

        # Adding model 'PlacetypeComponent'
        db.create_table('main_placetypecomponent', (
            ('builtform_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.BuiltForm'], unique=True, primary_key=True)),
            ('component_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.PlacetypeComponentCategory'])),
        ))
        db.send_create_signal('main', ['PlacetypeComponent'])

        # Adding model 'StreetAttributeSet'
        db.create_table('main_streetattributeset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lane_width', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=4)),
            ('number_of_lanes', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=4)),
            ('block_size', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=4)),
        ))
        db.send_create_signal('main', ['StreetAttributeSet'])

        # Adding model 'Placetype'
        db.create_table('main_placetype', (
            ('builtform_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.BuiltForm'], unique=True, primary_key=True)),
            ('street_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.StreetAttributeSet'], null=True)),
            ('intersection_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=4)),
        ))
        db.send_create_signal('main', ['Placetype'])

        # Adding model 'FlatBuiltForm'
        db.create_table('main_flatbuiltform', (
            ('built_form_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('intersection_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('built_form_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('gross_net_ratio', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=11, decimal_places=10)),
            ('dwelling_unit_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('household_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('population_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('employment_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('single_family_large_lot_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('single_family_small_lot_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('attached_single_family_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('multifamily_2_to_4_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('multifamily_5_plus_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('retail_services_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('restaurant_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('arts_entertainment_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('accommodation_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('other_services_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('office_services_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('public_admin_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('education_services_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('medical_services_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('manufacturing_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('wholesale_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('transport_warehouse_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('construction_utilities_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('agriculture_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('extraction_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('armed_forces_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('office_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('retail_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('industrial_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('residential_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('agricultural_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('acres_parcel_mixed_use', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('acres_parcel_residential', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('acres_parcel_employment', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('acres_parcel_mixed_use_with_office', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('acres_parcel_mixed_use_without_office', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('acres_parcel_residential_single_family_small_lot', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('acres_parcel_residential_single_family_large_lot', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('acres_parcel_residential_attached_single_family', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('acres_parcel_residential_multifamily', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('acres_parcel_employment_office', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('acres_parcel_employment_retail', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('acres_parcel_employment_industrial', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('acres_parcel_employment_agriculture', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('acres_parcel_employment_mixed', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=10)),
            ('building_sqft_total', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_detached_single_family', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_single_family_small_lot', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_single_family_large_lot', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_attached_single_family', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_multifamily_2_to_4', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_multifamily_5_plus', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_retail_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_restaurant', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_accommodation', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_arts_entertainment', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_other_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_office_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_public_admin', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_education_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_medical_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_wholesale', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_transport_warehouse', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('building_sqft_industrial_non_warehouse', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('residential_irrigated_square_feet', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('commercial_irrigated_square_feet', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=7)),
            ('softscape_and_landscape_percent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=7)),
            ('irrigated_percent', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=15, decimal_places=7)),
            ('percent_streets', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=6, decimal_places=5)),
            ('percent_parks', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=6, decimal_places=5)),
            ('percent_civic', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=6, decimal_places=5)),
            ('percent_mixed_use', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=6, decimal_places=5)),
            ('percent_residential', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=6, decimal_places=5)),
            ('percent_employment', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=6, decimal_places=5)),
            ('pt_density', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('pt_connectivity', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('pt_land_use_mix', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('pt_score', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('intersections_sqmi', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('avg_estimated_building_height_feet', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('building_avg_number_of_floors', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('block_avg_size_acres', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('street_pattern', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal('main', ['FlatBuiltForm'])

        # Adding model 'Core'
        db.create_table('main_core', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('config_entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ConfigEntity'])),
            ('celery_task', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('previous_celery_task', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('started', self.gf('django.db.models.fields.DateField')(null=True)),
            ('completed', self.gf('django.db.models.fields.DateField')(null=True)),
            ('failed', self.gf('django.db.models.fields.DateField')(null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal('main', ['Core'])

        # Adding model 'Fiscal'
        db.create_table('main_fiscal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('config_entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ConfigEntity'])),
            ('celery_task', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('previous_celery_task', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('started', self.gf('django.db.models.fields.DateField')(null=True)),
            ('completed', self.gf('django.db.models.fields.DateField')(null=True)),
            ('failed', self.gf('django.db.models.fields.DateField')(null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal('main', ['Fiscal'])

        # Adding model 'Vmt'
        db.create_table('main_vmt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('config_entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ConfigEntity'])),
            ('celery_task', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('previous_celery_task', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('started', self.gf('django.db.models.fields.DateField')(null=True)),
            ('completed', self.gf('django.db.models.fields.DateField')(null=True)),
            ('failed', self.gf('django.db.models.fields.DateField')(null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal('main', ['Vmt'])

        # Adding model 'PrimaryComponentPercent'
        db.create_table('main_primarycomponentpercent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percent', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=21, decimal_places=20)),
            ('primary_component', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.PrimaryComponent'])),
            ('placetype_component', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.PlacetypeComponent'])),
        ))
        db.send_create_signal('main', ['PrimaryComponentPercent'])

        # Adding model 'PlacetypeComponentPercent'
        db.create_table('main_placetypecomponentpercent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percent', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=21, decimal_places=20)),
            ('placetype_component', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.PlacetypeComponent'], null=True)),
            ('placetype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Placetype'])),
        ))
        db.send_create_signal('main', ['PlacetypeComponentPercent'])

        # Adding model 'Interest'
        db.create_table('main_interest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
        ))
        db.send_create_signal('main', ['Interest'])

        # Adding model 'DbEntityInterest'
        db.create_table('main_dbentityinterest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('config_entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ConfigEntity'])),
            ('db_entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.DbEntity'])),
            ('interest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Interest'])),
        ))
        db.send_create_signal('main', ['DbEntityInterest'])

        # Adding model 'GlobalConfig'
        db.create_table('main_globalconfig', (
            ('configentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.ConfigEntity'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('main', ['GlobalConfig'])

        # Adding model 'Region'
        db.create_table('main_region', (
            ('configentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.ConfigEntity'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('main', ['Region'])

        # Adding model 'Project'
        db.create_table('main_project', (
            ('configentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.ConfigEntity'], unique=True, primary_key=True)),
            ('base_year', self.gf('django.db.models.fields.IntegerField')(default=2005)),
        ))
        db.send_create_signal('main', ['Project'])

        # Adding model 'Scenario'
        db.create_table('main_scenario', (
            ('configentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.ConfigEntity'], unique=True, primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('main', ['Scenario'])

        # Adding model 'BaseScenario'
        db.create_table('main_basescenario', (
            ('scenario_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Scenario'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('main', ['BaseScenario'])

        # Adding model 'FutureScenario'
        db.create_table('main_futurescenario', (
            ('scenario_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Scenario'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('main', ['FutureScenario'])

        # Adding model 'Parcel'
        db.create_table('main_parcel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wkb_geometry', self.gf('django.contrib.gis.db.models.fields.GeometryField')()),
        ))
        db.send_create_signal('main', ['Parcel'])

        # Adding model 'GridCell'
        db.create_table('main_gridcell', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.GeometryField')()),
            ('source_table_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('source_id', self.gf('django.db.models.fields.IntegerField')(max_length=200, db_index=True)),
        ))
        db.send_create_signal('main', ['GridCell'])

        # Adding model 'Taz'
        db.create_table('main_taz', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.GeometryField')()),
            ('source_table_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('source_id', self.gf('django.db.models.fields.IntegerField')(max_length=200, db_index=True)),
        ))
        db.send_create_signal('main', ['Taz'])

        # Adding model 'Result'
        db.create_table('main_result', (
            ('presentationmedium_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.PresentationMedium'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('main', ['Result'])

        # Adding model 'Chart'
        db.create_table('main_chart', (
            ('result_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Result'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('main', ['Chart'])

        # Adding model 'GeoLibrary'
        db.create_table('main_geolibrary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('main', ['GeoLibrary'])

        # Adding model 'GeoLibraryCatalog'
        db.create_table('main_geolibrarycatalog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.DbEntity'])),
            ('geo_library', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.GeoLibrary'])),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('main', ['GeoLibraryCatalog'])

        # Adding model 'Grid'
        db.create_table('main_grid', (
            ('result_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Result'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('main', ['Grid'])

        # Adding model 'LayerChart'
        db.create_table('main_layerchart', (
            ('chart_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Chart'], unique=True, primary_key=True)),
            ('layer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Layer'])),
        ))
        db.send_create_signal('main', ['LayerChart'])

        # Adding model 'Presentation'
        db.create_table('main_presentation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('scope', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('configuration', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('config_entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ConfigEntity'])),
        ))
        db.send_create_signal('main', ['Presentation'])

        # Adding model 'LayerLibrary'
        db.create_table('main_layerlibrary', (
            ('presentation_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Presentation'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('main', ['LayerLibrary'])

        # Adding model 'Map'
        db.create_table('main_map', (
            ('presentation_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Presentation'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('main', ['Map'])

        # Adding model 'Painting'
        db.create_table('main_painting', (
            ('map_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Map'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('main', ['Painting'])

        # Adding model 'Report'
        db.create_table('main_report', (
            ('presentation_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Presentation'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('main', ['Report'])

        # Adding model 'ResultLibrary'
        db.create_table('main_resultlibrary', (
            ('presentation_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Presentation'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('main', ['ResultLibrary'])

        # Adding model 'Style'
        db.create_table('main_style', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('identifier', self.gf('django.db.models.fields.TextField')()),
            ('target', self.gf('django.db.models.fields.TextField')()),
            ('style_property', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('main', ['Style'])

        # Adding model 'Template'
        db.create_table('main_template', (
            ('medium_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Medium'], unique=True, primary_key=True)),
            ('template_context', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('main', ['Template'])

        # Adding model 'PresentationConfiguration'
        db.create_table('main_presentationconfiguration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('scope', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('data', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('main', ['PresentationConfiguration'])

        # Adding model 'SortType'
        db.create_table('main_sorttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('order_by', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, unique=True, null=True)),
        ))
        db.send_create_signal('main', ['SortType'])

        # Adding model 'TileStacheConfig'
        db.create_table('main_tilestacheconfig', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='default', max_length=50)),
            ('config', self.gf('picklefield.fields.PickledObjectField')()),
            ('enable_caching', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
        ))
        db.send_create_signal('main', ['TileStacheConfig'])

        # Adding model 'SacogLandUseDefinition'
        db.create_table('main_sacoglandusedefinition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('land_use', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('min_du_ac', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('max_du_ac', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('max_emp_ac', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('rural_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('detached_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('attached_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pct_ret_rest', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('pct_ret_ret', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('pct_ret_svc', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('pct_off_gov', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('pct_off_off', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('pct_off_svc', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('pct_off_med', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('pct_ind', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('pct_pub_edu', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('pct_pub_med', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('pct_pub_gov', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
            ('pct_other', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2)),
        ))
        db.send_create_signal('main', ['SacogLandUseDefinition'])

        # Adding model 'SacogLandUse'
        db.create_table('main_sacoglanduse', (
            ('builtform_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.BuiltForm'], unique=True, primary_key=True)),
            ('land_use_definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.SacogLandUseDefinition'])),
        ))
        db.send_create_signal('main', ['SacogLandUse'])

        # Adding model 'ScagLandUseDefinition'
        db.create_table('main_scaglandusedefinition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('land_use_description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('land_use_type', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('land_use', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('main', ['ScagLandUseDefinition'])

        # Adding model 'ScagLandUse'
        db.create_table('main_scaglanduse', (
            ('builtform_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.BuiltForm'], unique=True, primary_key=True)),
            ('land_use_definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ScagLandUseDefinition'])),
        ))
        db.send_create_signal('main', ['ScagLandUse'])


    def backwards(self, orm):
        # Deleting model 'BuildingUsePercent'
        db.delete_table('main_buildingusepercent')

        # Deleting model 'BuildingUseDefinition'
        db.delete_table('main_buildingusedefinition')

        # Deleting model 'BuildingAttributeSet'
        db.delete_table('main_buildingattributeset')

        # Deleting model 'Tag'
        db.delete_table('main_tag')

        # Deleting model 'Medium'
        db.delete_table('main_medium')

        # Deleting model 'BuiltFormExample'
        db.delete_table('main_builtformexample')

        # Deleting model 'BuiltForm'
        db.delete_table('main_builtform')

        # Removing M2M table for field tags on 'BuiltForm'
        db.delete_table('main_builtform_tags')

        # Removing M2M table for field media on 'BuiltForm'
        db.delete_table('main_builtform_media')

        # Removing M2M table for field examples on 'BuiltForm'
        db.delete_table('main_builtform_examples')

        # Deleting model 'DbEntity'
        db.delete_table('main_dbentity')

        # Removing M2M table for field tags on 'DbEntity'
        db.delete_table('main_dbentity_tags')

        # Deleting model 'Category'
        db.delete_table('main_category')

        # Deleting model 'BuiltFormSet'
        db.delete_table('main_builtformset')

        # Removing M2M table for field built_forms on 'BuiltFormSet'
        db.delete_table('main_builtformset_built_forms')

        # Deleting model 'Policy'
        db.delete_table('main_policy')

        # Removing M2M table for field tags on 'Policy'
        db.delete_table('main_policy_tags')

        # Removing M2M table for field policies on 'Policy'
        db.delete_table('main_policy_policies')

        # Deleting model 'PolicySet'
        db.delete_table('main_policyset')

        # Removing M2M table for field policies on 'PolicySet'
        db.delete_table('main_policyset_policies')

        # Deleting model 'ConfigEntity'
        db.delete_table('main_configentity')

        # Removing M2M table for field categories on 'ConfigEntity'
        db.delete_table('main_configentity_categories')

        # Removing M2M table for field built_form_sets on 'ConfigEntity'
        db.delete_table('main_configentity_built_form_sets')

        # Removing M2M table for field policy_sets on 'ConfigEntity'
        db.delete_table('main_configentity_policy_sets')

        # Removing M2M table for field media on 'ConfigEntity'
        db.delete_table('main_configentity_media')

        # Deleting model 'Job'
        db.delete_table('main_job')

        # Deleting model 'PresentationMedium'
        db.delete_table('main_presentationmedium')

        # Removing M2M table for field tags on 'PresentationMedium'
        db.delete_table('main_presentationmedium_tags')

        # Deleting model 'Layer'
        db.delete_table('main_layer')

        # Deleting model 'PrimaryComponent'
        db.delete_table('main_primarycomponent')

        # Deleting model 'PlacetypeComponentCategory'
        db.delete_table('main_placetypecomponentcategory')

        # Deleting model 'PlacetypeComponent'
        db.delete_table('main_placetypecomponent')

        # Deleting model 'StreetAttributeSet'
        db.delete_table('main_streetattributeset')

        # Deleting model 'Placetype'
        db.delete_table('main_placetype')

        # Deleting model 'FlatBuiltForm'
        db.delete_table('main_flatbuiltform')

        # Deleting model 'Core'
        db.delete_table('main_core')

        # Deleting model 'Fiscal'
        db.delete_table('main_fiscal')

        # Deleting model 'Vmt'
        db.delete_table('main_vmt')

        # Deleting model 'PrimaryComponentPercent'
        db.delete_table('main_primarycomponentpercent')

        # Deleting model 'PlacetypeComponentPercent'
        db.delete_table('main_placetypecomponentpercent')

        # Deleting model 'Interest'
        db.delete_table('main_interest')

        # Deleting model 'DbEntityInterest'
        db.delete_table('main_dbentityinterest')

        # Deleting model 'GlobalConfig'
        db.delete_table('main_globalconfig')

        # Deleting model 'Region'
        db.delete_table('main_region')

        # Deleting model 'Project'
        db.delete_table('main_project')

        # Deleting model 'Scenario'
        db.delete_table('main_scenario')

        # Deleting model 'BaseScenario'
        db.delete_table('main_basescenario')

        # Deleting model 'FutureScenario'
        db.delete_table('main_futurescenario')

        # Deleting model 'Parcel'
        db.delete_table('main_parcel')

        # Deleting model 'GridCell'
        db.delete_table('main_gridcell')

        # Deleting model 'Taz'
        db.delete_table('main_taz')

        # Deleting model 'Result'
        db.delete_table('main_result')

        # Deleting model 'Chart'
        db.delete_table('main_chart')

        # Deleting model 'GeoLibrary'
        db.delete_table('main_geolibrary')

        # Deleting model 'GeoLibraryCatalog'
        db.delete_table('main_geolibrarycatalog')

        # Deleting model 'Grid'
        db.delete_table('main_grid')

        # Deleting model 'LayerChart'
        db.delete_table('main_layerchart')

        # Deleting model 'Presentation'
        db.delete_table('main_presentation')

        # Deleting model 'LayerLibrary'
        db.delete_table('main_layerlibrary')

        # Deleting model 'Map'
        db.delete_table('main_map')

        # Deleting model 'Painting'
        db.delete_table('main_painting')

        # Deleting model 'Report'
        db.delete_table('main_report')

        # Deleting model 'ResultLibrary'
        db.delete_table('main_resultlibrary')

        # Deleting model 'Style'
        db.delete_table('main_style')

        # Deleting model 'Template'
        db.delete_table('main_template')

        # Deleting model 'PresentationConfiguration'
        db.delete_table('main_presentationconfiguration')

        # Deleting model 'SortType'
        db.delete_table('main_sorttype')

        # Deleting model 'TileStacheConfig'
        db.delete_table('main_tilestacheconfig')

        # Deleting model 'SacogLandUseDefinition'
        db.delete_table('main_sacoglandusedefinition')

        # Deleting model 'SacogLandUse'
        db.delete_table('main_sacoglanduse')

        # Deleting model 'ScagLandUseDefinition'
        db.delete_table('main_scaglandusedefinition')

        # Deleting model 'ScagLandUse'
        db.delete_table('main_scaglanduse')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.basescenario': {
            'Meta': {'object_name': 'BaseScenario', '_ormbases': ['main.Scenario']},
            'scenario_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.Scenario']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.buildingattributeset': {
            'Meta': {'object_name': 'BuildingAttributeSet'},
            'building_uses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.BuildingUseDefinition']", 'through': "orm['main.BuildingUsePercent']", 'symmetrical': 'False'}),
            'combined_pop_emp_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '4'}),
            'commercial_irrigated_square_feet': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2'}),
            'floors': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '3'}),
            'gross_net_ratio': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '8', 'decimal_places': '7'}),
            'gross_population_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '10'}),
            'hardscape_percent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3'}),
            'household_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impervious_hardscape_percent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3'}),
            'impervious_roof_percent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3'}),
            'irrigated_percent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3'}),
            'parking_spaces': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '3'}),
            'parking_structure_square_feet': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'pervious_hardscape_percent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3'}),
            'residential_average_lot_size': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2'}),
            'residential_irrigated_square_feet': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2'}),
            'softscape_and_landscape_percent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3'}),
            'total_far': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '7'})
        },
        'main.buildingusedefinition': {
            'Meta': {'object_name': 'BuildingUseDefinition'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.BuildingUseDefinition']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.buildingusepercent': {
            'Meta': {'object_name': 'BuildingUsePercent'},
            'building_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.BuildingAttributeSet']"}),
            'building_use_definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.BuildingUseDefinition']"}),
            'efficiency': ('django.db.models.fields.DecimalField', [], {'default': '0.85', 'max_digits': '6', 'decimal_places': '4'}),
            'floor_area_ratio': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '10'}),
            'gross_built_up_area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '13', 'decimal_places': '3'}),
            'household_size': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'net_built_up_area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '13', 'decimal_places': '3'}),
            'percent': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '21', 'decimal_places': '20'}),
            'square_feet_per_unit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '3'}),
            'unit_density': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '10'}),
            'vacancy_rate': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '3'})
        },
        'main.builtform': {
            'Meta': {'object_name': 'BuiltForm'},
            'building_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.BuildingAttributeSet']", 'null': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'examples': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.BuiltFormExample']", 'null': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'built_form_media'", 'symmetrical': 'False', 'to': "orm['main.Medium']"}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Medium']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'origin_built_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.BuiltForm']", 'null': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Tag']", 'symmetrical': 'False'})
        },
        'main.builtformexample': {
            'Meta': {'object_name': 'BuiltFormExample'},
            'content': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url_aerial': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'url_street': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'main.builtformset': {
            'Meta': {'object_name': 'BuiltFormSet'},
            'built_forms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.BuiltForm']", 'symmetrical': 'False'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.chart': {
            'Meta': {'object_name': 'Chart', '_ormbases': ['main.Result']},
            'result_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.Result']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.configentity': {
            'Meta': {'object_name': 'ConfigEntity'},
            'bounds': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'built_form_sets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.BuiltFormSet']", 'symmetrical': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Category']", 'symmetrical': 'False'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_entity_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'db_entities': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.DbEntity']", 'through': "orm['main.DbEntityInterest']", 'symmetrical': 'False'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Medium']", 'null': 'True', 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'origin_config_entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clone_set'", 'null': 'True', 'to': "orm['main.ConfigEntity']"}),
            'parent_config_entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_set'", 'null': 'True', 'to': "orm['main.ConfigEntity']"}),
            'policy_sets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.PolicySet']", 'symmetrical': 'False'}),
            'scope': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'selections': ('footprint.main.models.config.model_pickled_object_field.SelectionModelsPickledObjectField', [], {'default': "{'db_entities': {}, 'sets': {}}"}),
            'updater': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_entity_updater'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'main.core': {
            'Meta': {'object_name': 'Core'},
            'celery_task': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'completed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'config_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.ConfigEntity']"}),
            'failed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'previous_celery_task': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'started': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'main.dbentity': {
            'Meta': {'object_name': 'DbEntity'},
            'class_key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_entity_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extent_authority': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'feature_class_configuration': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'group_by': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'hosts': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'query': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'schema': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'srid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'table': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Tag']", 'symmetrical': 'False'}),
            'updater': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_entity_updater'", 'null': 'True', 'to': "orm['auth.User']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'})
        },
        'main.dbentityinterest': {
            'Meta': {'object_name': 'DbEntityInterest'},
            'config_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.ConfigEntity']"}),
            'db_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.DbEntity']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Interest']"})
        },
        'main.fiscal': {
            'Meta': {'object_name': 'Fiscal'},
            'celery_task': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'completed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'config_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.ConfigEntity']"}),
            'failed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'previous_celery_task': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'started': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'main.flatbuiltform': {
            'Meta': {'object_name': 'FlatBuiltForm'},
            'accommodation_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'acres_parcel_employment': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'acres_parcel_employment_agriculture': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'acres_parcel_employment_industrial': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'acres_parcel_employment_mixed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'acres_parcel_employment_office': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'acres_parcel_employment_retail': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'acres_parcel_mixed_use': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'acres_parcel_mixed_use_with_office': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'acres_parcel_mixed_use_without_office': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'acres_parcel_residential': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'acres_parcel_residential_attached_single_family': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'acres_parcel_residential_multifamily': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'acres_parcel_residential_single_family_large_lot': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'acres_parcel_residential_single_family_small_lot': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'agricultural_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'agriculture_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'armed_forces_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'arts_entertainment_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'attached_single_family_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'avg_estimated_building_height_feet': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'block_avg_size_acres': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'building_avg_number_of_floors': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'building_sqft_accommodation': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_arts_entertainment': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_attached_single_family': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_detached_single_family': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_education_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_industrial_non_warehouse': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_medical_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_multifamily_2_to_4': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_multifamily_5_plus': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_office_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_other_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_public_admin': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_restaurant': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_retail_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_single_family_large_lot': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_single_family_small_lot': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_total': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_transport_warehouse': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'building_sqft_wholesale': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'built_form_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'built_form_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'commercial_irrigated_square_feet': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'construction_utilities_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dwelling_unit_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'education_services_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'employment_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'extraction_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'gross_net_ratio': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '10'}),
            'household_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'industrial_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'intersection_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'intersections_sqmi': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'irrigated_percent': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '15', 'decimal_places': '7'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'manufacturing_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'medical_services_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'multifamily_2_to_4_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'multifamily_5_plus_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'office_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'office_services_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'other_services_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'percent_civic': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '5'}),
            'percent_employment': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '5'}),
            'percent_mixed_use': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '5'}),
            'percent_parks': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '5'}),
            'percent_residential': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '5'}),
            'percent_streets': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '5'}),
            'population_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'pt_connectivity': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pt_density': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pt_land_use_mix': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pt_score': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'public_admin_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'residential_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'residential_irrigated_square_feet': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '7'}),
            'restaurant_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'retail_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'retail_services_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'single_family_large_lot_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'single_family_small_lot_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'softscape_and_landscape_percent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '7'}),
            'street_pattern': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'transport_warehouse_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'wholesale_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'})
        },
        'main.futurescenario': {
            'Meta': {'object_name': 'FutureScenario', '_ormbases': ['main.Scenario']},
            'scenario_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.Scenario']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.geolibrary': {
            'Meta': {'object_name': 'GeoLibrary'},
            'entities': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.DbEntity']", 'through': "orm['main.GeoLibraryCatalog']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.geolibrarycatalog': {
            'Meta': {'object_name': 'GeoLibraryCatalog'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.DbEntity']"}),
            'geo_library': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.GeoLibrary']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.globalconfig': {
            'Meta': {'object_name': 'GlobalConfig', '_ormbases': ['main.ConfigEntity']},
            'configentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.ConfigEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.grid': {
            'Meta': {'object_name': 'Grid', '_ormbases': ['main.Result']},
            'result_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.Result']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.gridcell': {
            'Meta': {'object_name': 'GridCell'},
            'geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_id': ('django.db.models.fields.IntegerField', [], {'max_length': '200', 'db_index': 'True'}),
            'source_table_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        'main.interest': {
            'Meta': {'object_name': 'Interest'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'})
        },
        'main.job': {
            'Meta': {'ordering': "['-created_on']", 'object_name': 'Job'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'ended_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'hashid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobs'", 'to': "orm['auth.User']"})
        },
        'main.layer': {
            'Meta': {'object_name': 'Layer', '_ormbases': ['main.PresentationMedium']},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'presentationmedium_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.PresentationMedium']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.layerchart': {
            'Meta': {'object_name': 'LayerChart', '_ormbases': ['main.Chart']},
            'chart_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.Chart']", 'unique': 'True', 'primary_key': 'True'}),
            'layer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Layer']"})
        },
        'main.layerlibrary': {
            'Meta': {'object_name': 'LayerLibrary', '_ormbases': ['main.Presentation']},
            'presentation_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.Presentation']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.map': {
            'Meta': {'object_name': 'Map', '_ormbases': ['main.Presentation']},
            'presentation_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.Presentation']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.medium': {
            'Meta': {'object_name': 'Medium'},
            'content': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'main.painting': {
            'Meta': {'object_name': 'Painting', '_ormbases': ['main.Map']},
            'map_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.Map']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.parcel': {
            'Meta': {'object_name': 'Parcel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'wkb_geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {})
        },
        'main.placetype': {
            'Meta': {'object_name': 'Placetype', '_ormbases': ['main.BuiltForm']},
            'builtform_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.BuiltForm']", 'unique': 'True', 'primary_key': 'True'}),
            'intersection_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '4'}),
            'placetype_components': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.PlacetypeComponent']", 'through': "orm['main.PlacetypeComponentPercent']", 'symmetrical': 'False'}),
            'street_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.StreetAttributeSet']", 'null': 'True'})
        },
        'main.placetypecomponent': {
            'Meta': {'object_name': 'PlacetypeComponent', '_ormbases': ['main.BuiltForm']},
            'builtform_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.BuiltForm']", 'unique': 'True', 'primary_key': 'True'}),
            'component_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.PlacetypeComponentCategory']"}),
            'primary_components': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.PrimaryComponent']", 'through': "orm['main.PrimaryComponentPercent']", 'symmetrical': 'False'})
        },
        'main.placetypecomponentcategory': {
            'Meta': {'object_name': 'PlacetypeComponentCategory'},
            'contributes_to_net': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.placetypecomponentpercent': {
            'Meta': {'object_name': 'PlacetypeComponentPercent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '21', 'decimal_places': '20'}),
            'placetype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Placetype']"}),
            'placetype_component': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.PlacetypeComponent']", 'null': 'True'})
        },
        'main.policy': {
            'Meta': {'object_name': 'Policy'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'policies': ('django.db.models.fields.related.ManyToManyField', [], {'default': '[]', 'to': "orm['main.Policy']", 'symmetrical': 'False'}),
            'schema': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Tag']", 'symmetrical': 'False'}),
            'values': ('picklefield.fields.PickledObjectField', [], {})
        },
        'main.policyset': {
            'Meta': {'object_name': 'PolicySet'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'policies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Policy']", 'symmetrical': 'False'})
        },
        'main.presentation': {
            'Meta': {'object_name': 'Presentation'},
            'config_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.ConfigEntity']"}),
            'configuration': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'scope': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'main.presentationconfiguration': {
            'Meta': {'object_name': 'PresentationConfiguration'},
            'data': ('picklefield.fields.PickledObjectField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'scope': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'main.presentationmedium': {
            'Meta': {'object_name': 'PresentationMedium'},
            'configuration': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'db_entity_key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Medium']"}),
            'medium_context': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'presentation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Presentation']"}),
            'rendered_medium': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Tag']", 'symmetrical': 'False'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'visible_attributes': ('picklefield.fields.PickledObjectField', [], {'null': 'True'})
        },
        'main.primarycomponent': {
            'Meta': {'object_name': 'PrimaryComponent', '_ormbases': ['main.BuiltForm']},
            'builtform_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.BuiltForm']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.primarycomponentpercent': {
            'Meta': {'object_name': 'PrimaryComponentPercent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '21', 'decimal_places': '20'}),
            'placetype_component': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.PlacetypeComponent']"}),
            'primary_component': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.PrimaryComponent']"})
        },
        'main.project': {
            'Meta': {'object_name': 'Project', '_ormbases': ['main.ConfigEntity']},
            'base_year': ('django.db.models.fields.IntegerField', [], {'default': '2005'}),
            'configentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.ConfigEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.region': {
            'Meta': {'object_name': 'Region', '_ormbases': ['main.ConfigEntity']},
            'configentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.ConfigEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.report': {
            'Meta': {'object_name': 'Report', '_ormbases': ['main.Presentation']},
            'presentation_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.Presentation']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.result': {
            'Meta': {'object_name': 'Result', '_ormbases': ['main.PresentationMedium']},
            'presentationmedium_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.PresentationMedium']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.resultlibrary': {
            'Meta': {'object_name': 'ResultLibrary', '_ormbases': ['main.Presentation']},
            'presentation_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.Presentation']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.sacoglanduse': {
            'Meta': {'object_name': 'SacogLandUse'},
            'builtform_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.BuiltForm']", 'unique': 'True', 'primary_key': 'True'}),
            'land_use_definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.SacogLandUseDefinition']"})
        },
        'main.sacoglandusedefinition': {
            'Meta': {'object_name': 'SacogLandUseDefinition'},
            'attached_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'detached_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_use': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'max_du_ac': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'max_emp_ac': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'min_du_ac': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'pct_ind': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'pct_off_gov': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'pct_off_med': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'pct_off_off': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'pct_off_svc': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'pct_other': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'pct_pub_edu': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'pct_pub_gov': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'pct_pub_med': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'pct_ret_rest': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'pct_ret_ret': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'pct_ret_svc': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '2'}),
            'rural_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'main.scaglanduse': {
            'Meta': {'object_name': 'ScagLandUse'},
            'builtform_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.BuiltForm']", 'unique': 'True', 'primary_key': 'True'}),
            'land_use_definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.ScagLandUseDefinition']"})
        },
        'main.scaglandusedefinition': {
            'Meta': {'object_name': 'ScagLandUseDefinition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_use': ('django.db.models.fields.IntegerField', [], {}),
            'land_use_description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'land_use_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'main.scenario': {
            'Meta': {'object_name': 'Scenario', '_ormbases': ['main.ConfigEntity']},
            'configentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.ConfigEntity']", 'unique': 'True', 'primary_key': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.sorttype': {
            'Meta': {'object_name': 'SortType'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order_by': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'unique': 'True', 'null': 'True'})
        },
        'main.streetattributeset': {
            'Meta': {'object_name': 'StreetAttributeSet'},
            'block_size': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lane_width': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '4'}),
            'number_of_lanes': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '4'})
        },
        'main.style': {
            'Meta': {'object_name': 'Style'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.TextField', [], {}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'style_property': ('django.db.models.fields.TextField', [], {}),
            'target': ('django.db.models.fields.TextField', [], {})
        },
        'main.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.taz': {
            'Meta': {'object_name': 'Taz'},
            'geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_id': ('django.db.models.fields.IntegerField', [], {'max_length': '200', 'db_index': 'True'}),
            'source_table_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        'main.template': {
            'Meta': {'object_name': 'Template', '_ormbases': ['main.Medium']},
            'medium_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.Medium']", 'unique': 'True', 'primary_key': 'True'}),
            'template_context': ('picklefield.fields.PickledObjectField', [], {})
        },
        'main.tilestacheconfig': {
            'Meta': {'object_name': 'TileStacheConfig'},
            'config': ('picklefield.fields.PickledObjectField', [], {}),
            'enable_caching': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '50'})
        },
        'main.vmt': {
            'Meta': {'object_name': 'Vmt'},
            'celery_task': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'completed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'config_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.ConfigEntity']"}),
            'failed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'previous_celery_task': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'started': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        }
    }

    complete_apps = ['main']