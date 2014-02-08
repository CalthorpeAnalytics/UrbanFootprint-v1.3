# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Geography'
        db.create_table('footprint_geography', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.GeometryField')()),
            ('source_id', self.gf('django.db.models.fields.TextField')(max_length=200, db_index=True)),
        ))
        db.send_create_signal('footprint', ['Geography'])

        # Adding model 'BuildingUsePercent'
        db.create_table('footprint_buildingusepercent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percent', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=21, decimal_places=20)),
            ('building_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.BuildingAttributeSet'])),
            ('building_use_definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.BuildingUseDefinition'])),
            ('vacancy_rate', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=4, decimal_places=3)),
            ('household_size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3)),
            ('efficiency', self.gf('django.db.models.fields.DecimalField')(default=0.85, max_digits=6, decimal_places=4)),
            ('square_feet_per_unit', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=3)),
            ('floor_area_ratio', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=10)),
            ('unit_density', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10)),
            ('gross_built_up_area', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=13, decimal_places=3)),
            ('net_built_up_area', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=13, decimal_places=3)),
        ))
        db.send_create_signal('footprint', ['BuildingUsePercent'])

        # Adding model 'BuildingUseDefinition'
        db.create_table('footprint_buildingusedefinition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.BuildingUseDefinition'], null=True)),
        ))
        db.send_create_signal('footprint', ['BuildingUseDefinition'])

        # Adding model 'BuildingAttributeSet'
        db.create_table('footprint_buildingattributeset', (
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
        db.send_create_signal('footprint', ['BuildingAttributeSet'])

        # Adding model 'Tag'
        db.create_table('footprint_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('footprint', ['Tag'])

        # Adding model 'Medium'
        db.create_table('footprint_medium', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('content', self.gf('picklefield.fields.PickledObjectField')(null=True)),
        ))
        db.send_create_signal('footprint', ['Medium'])

        # Adding model 'BuiltFormExample'
        db.create_table('footprint_builtformexample', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('content', self.gf('picklefield.fields.PickledObjectField')(null=True)),
        ))
        db.send_create_signal('footprint', ['BuiltFormExample'])

        # Adding model 'BuiltForm'
        db.create_table('footprint_builtform', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('building_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.BuildingAttributeSet'], null=True)),
            ('origin_built_form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.BuiltForm'], null=True)),
            ('medium', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.Medium'], null=True)),
        ))
        db.send_create_signal('footprint', ['BuiltForm'])

        # Adding M2M table for field tags on 'BuiltForm'
        db.create_table('footprint_builtform_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('builtform', models.ForeignKey(orm['footprint.builtform'], null=False)),
            ('tag', models.ForeignKey(orm['footprint.tag'], null=False))
        ))
        db.create_unique('footprint_builtform_tags', ['builtform_id', 'tag_id'])

        # Adding M2M table for field media on 'BuiltForm'
        db.create_table('footprint_builtform_media', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('builtform', models.ForeignKey(orm['footprint.builtform'], null=False)),
            ('medium', models.ForeignKey(orm['footprint.medium'], null=False))
        ))
        db.create_unique('footprint_builtform_media', ['builtform_id', 'medium_id'])

        # Adding M2M table for field examples on 'BuiltForm'
        db.create_table('footprint_builtform_examples', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('builtform', models.ForeignKey(orm['footprint.builtform'], null=False)),
            ('builtformexample', models.ForeignKey(orm['footprint.builtformexample'], null=False))
        ))
        db.create_unique('footprint_builtform_examples', ['builtform_id', 'builtformexample_id'])

        # Adding model 'TemplateCoreEndStateFeature'
        db.create_table('footprint_templatecoreendstatefeature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geography', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.Geography'], null=True)),
            ('wkb_geometry', self.gf('django.contrib.gis.db.models.fields.GeometryField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('built_form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.BuiltForm'], null=True)),
            ('acres_gross', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res_detsf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res_detsf_ll', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res_detsf_sl', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res_attsf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res_mf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_ret', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_off', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_ind', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_ag', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_military', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_mixed', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_mixed_w_off', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_mixed_no_off', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_no_use', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_detsf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_detsf_ll', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_detsf_sl', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_attsf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_mf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_ret', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_retail_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_restaurant', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_accommodation', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_arts_entertainment', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_other_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_off', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_office_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_education', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_public_admin', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_medical_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_ind', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_wholesale', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_transport_warehousing', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_manufacturing', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_construction', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_utilities', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_ag', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_agriculture', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_extraction', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_military', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_detsf_ll', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_detsf_sl', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_attsf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_mf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_retail_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_restaurant', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_accommodation', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_arts_entertainment', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_other_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_office_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_public_admin', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_medical_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_education', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_wholesale', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_transport_warehousing', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('commercial_irrigated_sqft', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('residential_irrigated_sqft', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
        ))
        db.send_create_signal('footprint', ['TemplateCoreEndStateFeature'])

        # Adding model 'TemplateCoreIncrementFeature'
        db.create_table('footprint_templatecoreincrementfeature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geography', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.Geography'], null=True)),
            ('wkb_geometry', self.gf('django.contrib.gis.db.models.fields.GeometryField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('pop', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('hh', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('du', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('du_detsf', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('du_detsf_ll', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('du_detsf_sl', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('du_attsf', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('du_mf', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_ret', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_retail_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_restaurant', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_accommodation', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_arts_entertainment', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_other_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_off', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_office_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_education', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_public_admin', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_medical_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_ind', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_wholesale', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_transport_warehousing', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_manufacturing', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_utilities', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_construction', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_ag', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_agriculture', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_extraction', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_military', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('refill', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('footprint', ['TemplateCoreIncrementFeature'])

        # Adding model 'DbEntity'
        db.create_table('footprint_dbentity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('schema', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('table', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
            ('hosts', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('query', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('class_key', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('group_by', self.gf('picklefield.fields.PickledObjectField')(null=True)),
        ))
        db.send_create_signal('footprint', ['DbEntity'])

        # Adding M2M table for field tags on 'DbEntity'
        db.create_table('footprint_dbentity_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dbentity', models.ForeignKey(orm['footprint.dbentity'], null=False)),
            ('tag', models.ForeignKey(orm['footprint.tag'], null=False))
        ))
        db.create_unique('footprint_dbentity_tags', ['dbentity_id', 'tag_id'])

        # Adding model 'Category'
        db.create_table('footprint_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('footprint', ['Category'])

        # Adding model 'Interest'
        db.create_table('footprint_interest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
        ))
        db.send_create_signal('footprint', ['Interest'])

        # Adding model 'DbEntityInterest'
        db.create_table('footprint_dbentityinterest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('config_entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.ConfigEntity'])),
            ('db_entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.DbEntity'])),
            ('interest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.Interest'])),
        ))
        db.send_create_signal('footprint', ['DbEntityInterest'])

        # Adding model 'BuiltFormSet'
        db.create_table('footprint_builtformset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('footprint', ['BuiltFormSet'])

        # Adding M2M table for field built_forms on 'BuiltFormSet'
        db.create_table('footprint_builtformset_built_forms', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('builtformset', models.ForeignKey(orm['footprint.builtformset'], null=False)),
            ('builtform', models.ForeignKey(orm['footprint.builtform'], null=False))
        ))
        db.create_unique('footprint_builtformset_built_forms', ['builtformset_id', 'builtform_id'])

        # Adding model 'Policy'
        db.create_table('footprint_policy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('values', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('footprint', ['Policy'])

        # Adding M2M table for field tags on 'Policy'
        db.create_table('footprint_policy_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('policy', models.ForeignKey(orm['footprint.policy'], null=False)),
            ('tag', models.ForeignKey(orm['footprint.tag'], null=False))
        ))
        db.create_unique('footprint_policy_tags', ['policy_id', 'tag_id'])

        # Adding M2M table for field policies on 'Policy'
        db.create_table('footprint_policy_policies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_policy', models.ForeignKey(orm['footprint.policy'], null=False)),
            ('to_policy', models.ForeignKey(orm['footprint.policy'], null=False))
        ))
        db.create_unique('footprint_policy_policies', ['from_policy_id', 'to_policy_id'])

        # Adding model 'PolicySet'
        db.create_table('footprint_policyset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('footprint', ['PolicySet'])

        # Adding M2M table for field policies on 'PolicySet'
        db.create_table('footprint_policyset_policies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('policyset', models.ForeignKey(orm['footprint.policyset'], null=False)),
            ('policy', models.ForeignKey(orm['footprint.policy'], null=False))
        ))
        db.create_unique('footprint_policyset_policies', ['policyset_id', 'policy_id'])

        # Adding model 'ConfigEntity'
        db.create_table('footprint_configentity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('scope', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('bounds', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('parent_config_entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent_set', null=True, to=orm['footprint.ConfigEntity'])),
            ('origin_config_entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='clone_set', null=True, to=orm['footprint.ConfigEntity'])),
            ('selections', self.gf('picklefield.fields.PickledObjectField')(default={'db_entities': {}, 'sets': {}})),
        ))
        db.send_create_signal('footprint', ['ConfigEntity'])

        # Adding M2M table for field categories on 'ConfigEntity'
        db.create_table('footprint_configentity_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('configentity', models.ForeignKey(orm['footprint.configentity'], null=False)),
            ('category', models.ForeignKey(orm['footprint.category'], null=False))
        ))
        db.create_unique('footprint_configentity_categories', ['configentity_id', 'category_id'])

        # Adding M2M table for field built_form_sets on 'ConfigEntity'
        db.create_table('footprint_configentity_built_form_sets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('configentity', models.ForeignKey(orm['footprint.configentity'], null=False)),
            ('builtformset', models.ForeignKey(orm['footprint.builtformset'], null=False))
        ))
        db.create_unique('footprint_configentity_built_form_sets', ['configentity_id', 'builtformset_id'])

        # Adding M2M table for field policy_sets on 'ConfigEntity'
        db.create_table('footprint_configentity_policy_sets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('configentity', models.ForeignKey(orm['footprint.configentity'], null=False)),
            ('policyset', models.ForeignKey(orm['footprint.policyset'], null=False))
        ))
        db.create_unique('footprint_configentity_policy_sets', ['configentity_id', 'policyset_id'])

        # Adding M2M table for field media on 'ConfigEntity'
        db.create_table('footprint_configentity_media', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('configentity', models.ForeignKey(orm['footprint.configentity'], null=False)),
            ('medium', models.ForeignKey(orm['footprint.medium'], null=False))
        ))
        db.create_unique('footprint_configentity_media', ['configentity_id', 'medium_id'])

        # Adding model 'TemplateEnergyWaterFeature'
        db.create_table('footprint_templateenergywaterfeature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geography', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.Geography'], null=True)),
            ('wkb_geometry', self.gf('django.contrib.gis.db.models.fields.GeometryField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('ResEnrgyNewConst', self.gf('django.db.models.fields.DecimalField')(default=30, max_digits=5, decimal_places=2)),
            ('ResEnrgyRetro', self.gf('django.db.models.fields.DecimalField')(default=0.5, max_digits=3, decimal_places=2)),
            ('ResEnrgyReplcmt', self.gf('django.db.models.fields.DecimalField')(default=0.6, max_digits=3, decimal_places=2)),
            ('ComEnrgyNewConst', self.gf('django.db.models.fields.DecimalField')(default=30, max_digits=5, decimal_places=2)),
            ('ComEnrgyRetro', self.gf('django.db.models.fields.DecimalField')(default=0.8, max_digits=3, decimal_places=2)),
            ('ComEnrgyReplcmt', self.gf('django.db.models.fields.DecimalField')(default=1.0, max_digits=3, decimal_places=2)),
            ('ResWatrNewConst', self.gf('django.db.models.fields.DecimalField')(default=30, max_digits=5, decimal_places=2)),
            ('ResWatrRetro', self.gf('django.db.models.fields.DecimalField')(default=0.05, max_digits=3, decimal_places=2)),
            ('ResWatrReplcmt', self.gf('django.db.models.fields.DecimalField')(default=0.06, max_digits=3, decimal_places=2)),
            ('ComIndWatrNewConst', self.gf('django.db.models.fields.DecimalField')(default=30, max_digits=5, decimal_places=2)),
            ('ComIndWatrRetro', self.gf('django.db.models.fields.DecimalField')(default=0.08, max_digits=3, decimal_places=2)),
            ('ComIndWatrReplcmt', self.gf('django.db.models.fields.DecimalField')(default=0.2, max_digits=3, decimal_places=2)),
            ('Water_GPCD_SF', self.gf('django.db.models.fields.IntegerField')(default=80)),
            ('Water_GPCD_MF', self.gf('django.db.models.fields.IntegerField')(default=70)),
            ('Water_GPED_Retail', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('Water_GPED_Office', self.gf('django.db.models.fields.IntegerField')(default=50)),
            ('Water_GPED_Industrial', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('Water_GPED_School', self.gf('django.db.models.fields.IntegerField')(default=86)),
            ('ann_ind_elec_peremp', self.gf('django.db.models.fields.FloatField')(default=27675.45)),
            ('ann_ind_gas_peremp', self.gf('django.db.models.fields.FloatField')(default=767.56)),
        ))
        db.send_create_signal('footprint', ['TemplateEnergyWaterFeature'])

        # Adding model 'Job'
        db.create_table('footprint_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hashid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36)),
            ('task_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jobs', to=orm['auth.User'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('status', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ended_on', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=10000, null=True)),
        ))
        db.send_create_signal('footprint', ['Job'])

        # Adding model 'TemplateBaseFeature'
        db.create_table('footprint_templatebasefeature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geography', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.Geography'], null=True)),
            ('wkb_geometry', self.gf('django.contrib.gis.db.models.fields.GeometryField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('built_form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.BuiltForm'], null=True, blank=True)),
            ('land_development_category', self.gf('django.db.models.fields.CharField')(default=None, max_length=250, null=True, blank=True)),
            ('region_lu_code', self.gf('django.db.models.fields.CharField')(default=None, max_length=250, null=True, blank=True)),
            ('landtype', self.gf('django.db.models.fields.CharField')(default=None, max_length=250, null=True, blank=True)),
            ('intersection_density_sqmi', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_gross', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('sqft_parcel', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res_detsf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res_detsf_sl', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res_detsf_ll', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res_attsf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res_mf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_off', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_ret', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_ind', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_ag', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_mixed', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_military', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_mixed', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_mixed_w_off', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_mixed_no_off', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_no_use', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_occupancy_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_detsf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_detsf_sl', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_detsf_ll', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_attsf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_mf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_mf2to4', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_mf5p', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_ret', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_retail_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_restaurant', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_accommodation', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_arts_entertainment', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_other_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_off', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_office_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_public_admin', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_education', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_medical_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_ind', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_manufacturing', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_wholesale', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_transport_warehousing', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_utilities', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_construction', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_ag', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_agriculture', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_extraction', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_military', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_detsf_sl', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_detsf_ll', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_attsf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_mf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_retail_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_restaurant', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_accommodation', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_arts_entertainment', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_other_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_office_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_public_admin', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_education', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_medical_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_wholesale', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_transport_warehousing', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('residential_irrigated_sqft', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('commercial_irrigated_sqft', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop_male', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop_female', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop_avg_age20_64', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop_female_age20_64', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop_male_age20_64', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop_age16_up', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop_age25_up', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop_age65_up', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop_age20_64', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop_hs_not_comp', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop_hs_diploma', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop_some_college', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop_college_degree', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop_graduate_degree', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop_employed', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_00_10', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_10_20', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_20_30', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_30_40', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_40_50', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_50_60', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_60_75', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_75_100', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_100_125', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_125_150', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_150_200', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_200p', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_avg_vehicles', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_avg_size', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_agg_inc', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_avg_inc', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_owner_occ', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_rental_occ', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
        ))
        db.send_create_signal('footprint', ['TemplateBaseFeature'])

        # Adding model 'TemplateDevelopableFeature'
        db.create_table('footprint_templatedevelopablefeature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geography', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.Geography'], null=True)),
            ('wkb_geometry', self.gf('django.contrib.gis.db.models.fields.GeometryField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('acres_gross', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_developable', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_urban', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_greenfield', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_constrained', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res_detsf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res_detsf_ll', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res_detsf_sl', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res_attsf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_res_mf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_ret', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_off', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_ind', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_ag', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_mixed', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_military', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_mixed', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_mixed_w_off', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_mixed_no_off', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('acres_parcel_no_use', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('pop', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_detsf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_detsf_ll', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_detsf_sl', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_attsf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('du_mf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_ret', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_retail_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_restaurant', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_accommodation', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_arts_entertainment', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_other_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_off', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_office_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_education', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_public_admin', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_medical_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_ind', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_wholesale', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_transport_warehousing', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_manufacturing', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_utilities', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_construction', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_ag', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_agriculture', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_extraction', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('emp_military', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_detsf_ll', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_detsf_sl', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_attsf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_mf', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_retail_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_restaurant', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_accommodation', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_arts_entertainment', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_other_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_office_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_public_admin', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_medical_services', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_education', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_wholesale', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('bldg_sqft_transport_warehousing', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('commercial_irrigated_sqft', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('residential_irrigated_sqft', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_00_10', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_10_20', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_20_30', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_30_40', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_40_50', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_50_60', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_60_75', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_75_100', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_100_125', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_125_150', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_150_200', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_inc_200p', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_agg_inc', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_owner_occ', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
            ('hh_rental_occ', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
        ))
        db.send_create_signal('footprint', ['TemplateDevelopableFeature'])

        # Adding model 'PresentationMedium'
        db.create_table('footprint_presentationmedium', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('presentation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.Presentation'])),
            ('medium', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.Medium'])),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('visible_attributes', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('db_entity_key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('medium_context', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('configuration', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('rendered_medium', self.gf('picklefield.fields.PickledObjectField')(null=True)),
        ))
        db.send_create_signal('footprint', ['PresentationMedium'])

        # Adding M2M table for field tags on 'PresentationMedium'
        db.create_table('footprint_presentationmedium_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('presentationmedium', models.ForeignKey(orm['footprint.presentationmedium'], null=False)),
            ('tag', models.ForeignKey(orm['footprint.tag'], null=False))
        ))
        db.create_unique('footprint_presentationmedium_tags', ['presentationmedium_id', 'tag_id'])

        # Adding model 'Layer'
        db.create_table('footprint_layer', (
            ('presentationmedium_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.PresentationMedium'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('footprint', ['Layer'])

        # Adding model 'TemplateScenarioBuiltFormFeature'
        db.create_table('footprint_templatescenariobuiltformfeature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geography', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.Geography'], null=True)),
            ('wkb_geometry', self.gf('django.contrib.gis.db.models.fields.GeometryField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('built_form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.BuiltForm'], null=True)),
            ('dev_pct', self.gf('django.db.models.fields.DecimalField')(default=1.0, max_digits=8, decimal_places=4)),
            ('density_pct', self.gf('django.db.models.fields.DecimalField')(default=1.0, max_digits=8, decimal_places=4)),
            ('total_redev', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dirty_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('refill_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('acres_gross', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_developable', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_developing', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel_res', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel_res_detsf_ll', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel_res_detsf_sl', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel_res_attsf', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel_res_mf', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel_emp', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_ret', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_off', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_ind', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_ag', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel_emp_mixed', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel_mixed', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel_mixed_w_off', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('acres_parcel_mixed_no_off', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('pop', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('hh', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('du', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('du_detsf_ll', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('du_detsf_sl', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('du_attsf', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('du_mf', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_ret', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_retail_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_restaurant', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_accommodation', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_arts_entertainment', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_other_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_off', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_office_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_education', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_public_admin', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_medical_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_ind', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_wholesale', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_transport_warehousing', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_manufacturing', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_construction_utilities', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_ag', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_agriculture', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_extraction', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('emp_military', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('bldg_sqft_detsf_ll', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('bldg_sqft_detsf_sl', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('bldg_sqft_attsf', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('bldg_sqft_mf', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('bldg_sqft_retail_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('bldg_sqft_restaurant', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('bldg_sqft_accommodation', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('bldg_sqft_arts_entertainment', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('bldg_sqft_other_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('bldg_sqft_office_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('bldg_sqft_public_admin', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('bldg_sqft_medical_services', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('bldg_sqft_education', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('bldg_sqft_wholesale', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('bldg_sqft_transport_warehousing', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('commercial_irrigated_sqft', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
            ('residential_irrigated_sqft', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=4)),
        ))
        db.send_create_signal('footprint', ['TemplateScenarioBuiltFormFeature'])

        # Adding model 'PrimaryComponent'
        db.create_table('footprint_primarycomponent', (
            ('builtform_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.BuiltForm'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('footprint', ['PrimaryComponent'])

        # Adding model 'PlacetypeComponentCategory'
        db.create_table('footprint_placetypecomponentcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contributes_to_net', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('footprint', ['PlacetypeComponentCategory'])

        # Adding model 'PlacetypeComponent'
        db.create_table('footprint_placetypecomponent', (
            ('builtform_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.BuiltForm'], unique=True, primary_key=True)),
            ('component_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.PlacetypeComponentCategory'])),
        ))
        db.send_create_signal('footprint', ['PlacetypeComponent'])

        # Adding model 'StreetAttributeSet'
        db.create_table('footprint_streetattributeset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lane_width', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=4)),
            ('number_of_lanes', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=4)),
            ('block_size', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=4)),
        ))
        db.send_create_signal('footprint', ['StreetAttributeSet'])

        # Adding model 'Placetype'
        db.create_table('footprint_placetype', (
            ('builtform_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.BuiltForm'], unique=True, primary_key=True)),
            ('street_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.StreetAttributeSet'], null=True)),
            ('intersection_density', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=4)),
        ))
        db.send_create_signal('footprint', ['Placetype'])

        # Adding model 'FlatBuiltForm'
        db.create_table('footprint_flatbuiltform', (
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
        ))
        db.send_create_signal('footprint', ['FlatBuiltForm'])

        # Adding model 'Core'
        db.create_table('footprint_core', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('config_entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.ConfigEntity'])),
            ('celery_task', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('previous_celery_task', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('started', self.gf('django.db.models.fields.DateField')(null=True)),
            ('completed', self.gf('django.db.models.fields.DateField')(null=True)),
            ('failed', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal('footprint', ['Core'])

        # Adding model 'PrimaryComponentPercent'
        db.create_table('footprint_primarycomponentpercent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percent', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=21, decimal_places=20)),
            ('primary_component', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.PrimaryComponent'])),
            ('placetype_component', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.PlacetypeComponent'])),
        ))
        db.send_create_signal('footprint', ['PrimaryComponentPercent'])

        # Adding model 'PlacetypeComponentPercent'
        db.create_table('footprint_placetypecomponentpercent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percent', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=21, decimal_places=20)),
            ('placetype_component', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.PlacetypeComponent'], null=True)),
            ('placetype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.Placetype'])),
        ))
        db.send_create_signal('footprint', ['PlacetypeComponentPercent'])

        # Adding model 'GlobalConfig'
        db.create_table('footprint_globalconfig', (
            ('configentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.ConfigEntity'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('footprint', ['GlobalConfig'])

        # Adding model 'Region'
        db.create_table('footprint_region', (
            ('configentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.ConfigEntity'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('footprint', ['Region'])

        # Adding model 'Project'
        db.create_table('footprint_project', (
            ('configentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.ConfigEntity'], unique=True, primary_key=True)),
            ('base_year', self.gf('django.db.models.fields.IntegerField')(default=2005)),
        ))
        db.send_create_signal('footprint', ['Project'])

        # Adding model 'Scenario'
        db.create_table('footprint_scenario', (
            ('configentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.ConfigEntity'], unique=True, primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('footprint', ['Scenario'])

        # Adding model 'BaseScenario'
        db.create_table('footprint_basescenario', (
            ('scenario_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.Scenario'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('footprint', ['BaseScenario'])

        # Adding model 'FutureScenario'
        db.create_table('footprint_futurescenario', (
            ('scenario_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.Scenario'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('footprint', ['FutureScenario'])

        # Adding model 'Parcel'
        db.create_table('footprint_parcel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geography', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.Geography'], null=True)),
            ('wkb_geometry', self.gf('django.contrib.gis.db.models.fields.GeometryField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('footprint', ['Parcel'])

        # Adding model 'GridCell'
        db.create_table('footprint_gridcell', (
            ('geography_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.Geography'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('footprint', ['GridCell'])

        # Adding model 'Taz'
        db.create_table('footprint_taz', (
            ('geography_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.Geography'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('footprint', ['Taz'])

        # Adding model 'Result'
        db.create_table('footprint_result', (
            ('presentationmedium_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.PresentationMedium'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('footprint', ['Result'])

        # Adding model 'Chart'
        db.create_table('footprint_chart', (
            ('result_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.Result'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('footprint', ['Chart'])

        # Adding model 'GeoLibrary'
        db.create_table('footprint_geolibrary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('footprint', ['GeoLibrary'])

        # Adding model 'GeoLibraryCatalog'
        db.create_table('footprint_geolibrarycatalog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.DbEntity'])),
            ('geo_library', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.GeoLibrary'])),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('footprint', ['GeoLibraryCatalog'])

        # Adding model 'Grid'
        db.create_table('footprint_grid', (
            ('result_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.Result'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('footprint', ['Grid'])

        # Adding model 'LayerChart'
        db.create_table('footprint_layerchart', (
            ('chart_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.Chart'], unique=True, primary_key=True)),
            ('layer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.Layer'])),
        ))
        db.send_create_signal('footprint', ['LayerChart'])

        # Adding model 'Presentation'
        db.create_table('footprint_presentation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('scope', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('configuration', self.gf('picklefield.fields.PickledObjectField')(null=True)),
            ('config_entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.ConfigEntity'])),
        ))
        db.send_create_signal('footprint', ['Presentation'])

        # Adding model 'LayerLibrary'
        db.create_table('footprint_layerlibrary', (
            ('presentation_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.Presentation'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('footprint', ['LayerLibrary'])

        # Adding model 'Map'
        db.create_table('footprint_map', (
            ('presentation_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.Presentation'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('footprint', ['Map'])

        # Adding model 'Painting'
        db.create_table('footprint_painting', (
            ('map_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.Map'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('footprint', ['Painting'])

        # Adding model 'Report'
        db.create_table('footprint_report', (
            ('presentation_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.Presentation'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('footprint', ['Report'])

        # Adding model 'ResultLibrary'
        db.create_table('footprint_resultlibrary', (
            ('presentation_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.Presentation'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('footprint', ['ResultLibrary'])

        # Adding M2M table for field results on 'ResultLibrary'
        db.create_table('footprint_resultlibrary_results', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resultlibrary', models.ForeignKey(orm['footprint.resultlibrary'], null=False)),
            ('result', models.ForeignKey(orm['footprint.result'], null=False))
        ))
        db.create_unique('footprint_resultlibrary_results', ['resultlibrary_id', 'result_id'])

        # Adding model 'Style'
        db.create_table('footprint_style', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('identifier', self.gf('django.db.models.fields.TextField')()),
            ('target', self.gf('django.db.models.fields.TextField')()),
            ('style_property', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('footprint', ['Style'])

        # Adding model 'Template'
        db.create_table('footprint_template', (
            ('medium_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.Medium'], unique=True, primary_key=True)),
            ('template_context', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('footprint', ['Template'])

        # Adding model 'PresentationConfiguration'
        db.create_table('footprint_presentationconfiguration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('scope', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('data', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('footprint', ['PresentationConfiguration'])

        # Adding model 'SortType'
        db.create_table('footprint_sorttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('order_by', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, unique=True, null=True)),
        ))
        db.send_create_signal('footprint', ['SortType'])

        # Adding model 'TileStacheConfig'
        db.create_table('footprint_tilestacheconfig', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='default', max_length=50)),
            ('config', self.gf('picklefield.fields.PickledObjectField')()),
            ('enable_caching', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
        ))
        db.send_create_signal('footprint', ['TileStacheConfig'])

        # Adding model 'SacogLandUseDefinition'
        db.create_table('footprint_sacoglandusedefinition', (
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
        db.send_create_signal('footprint', ['SacogLandUseDefinition'])

        # Adding model 'SacogLandUse'
        db.create_table('footprint_sacoglanduse', (
            ('builtform_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.BuiltForm'], unique=True, primary_key=True)),
            ('land_use_definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.SacogLandUseDefinition'])),
        ))
        db.send_create_signal('footprint', ['SacogLandUse'])

        # Adding model 'ScagLandUseDefinition'
        db.create_table('footprint_scaglandusedefinition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('land_use_description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('land_use_type', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('land_use', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('footprint', ['ScagLandUseDefinition'])

        # Adding model 'ScagLandUse'
        db.create_table('footprint_scaglanduse', (
            ('builtform_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.BuiltForm'], unique=True, primary_key=True)),
            ('land_use_definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.ScagLandUseDefinition'])),
        ))
        db.send_create_signal('footprint', ['ScagLandUse'])

        # Adding model 'DemoLandUseDefinition'
        db.create_table('footprint_demolandusedefinition', (
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
        db.send_create_signal('footprint', ['DemoLandUseDefinition'])

        # Adding model 'DemoLandUse'
        db.create_table('footprint_demolanduse', (
            ('builtform_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['footprint.BuiltForm'], unique=True, primary_key=True)),
            ('land_use_definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['footprint.DemoLandUseDefinition'])),
        ))
        db.send_create_signal('footprint', ['DemoLandUse'])


    def backwards(self, orm):
        # Deleting model 'Geography'
        db.delete_table('footprint_geography')

        # Deleting model 'BuildingUsePercent'
        db.delete_table('footprint_buildingusepercent')

        # Deleting model 'BuildingUseDefinition'
        db.delete_table('footprint_buildingusedefinition')

        # Deleting model 'BuildingAttributeSet'
        db.delete_table('footprint_buildingattributeset')

        # Deleting model 'Tag'
        db.delete_table('footprint_tag')

        # Deleting model 'Medium'
        db.delete_table('footprint_medium')

        # Deleting model 'BuiltFormExample'
        db.delete_table('footprint_builtformexample')

        # Deleting model 'BuiltForm'
        db.delete_table('footprint_builtform')

        # Removing M2M table for field tags on 'BuiltForm'
        db.delete_table('footprint_builtform_tags')

        # Removing M2M table for field media on 'BuiltForm'
        db.delete_table('footprint_builtform_media')

        # Removing M2M table for field examples on 'BuiltForm'
        db.delete_table('footprint_builtform_examples')

        # Deleting model 'TemplateCoreEndStateFeature'
        db.delete_table('footprint_templatecoreendstatefeature')

        # Deleting model 'TemplateCoreIncrementFeature'
        db.delete_table('footprint_templatecoreincrementfeature')

        # Deleting model 'DbEntity'
        db.delete_table('footprint_dbentity')

        # Removing M2M table for field tags on 'DbEntity'
        db.delete_table('footprint_dbentity_tags')

        # Deleting model 'Category'
        db.delete_table('footprint_category')

        # Deleting model 'Interest'
        db.delete_table('footprint_interest')

        # Deleting model 'DbEntityInterest'
        db.delete_table('footprint_dbentityinterest')

        # Deleting model 'BuiltFormSet'
        db.delete_table('footprint_builtformset')

        # Removing M2M table for field built_forms on 'BuiltFormSet'
        db.delete_table('footprint_builtformset_built_forms')

        # Deleting model 'Policy'
        db.delete_table('footprint_policy')

        # Removing M2M table for field tags on 'Policy'
        db.delete_table('footprint_policy_tags')

        # Removing M2M table for field policies on 'Policy'
        db.delete_table('footprint_policy_policies')

        # Deleting model 'PolicySet'
        db.delete_table('footprint_policyset')

        # Removing M2M table for field policies on 'PolicySet'
        db.delete_table('footprint_policyset_policies')

        # Deleting model 'ConfigEntity'
        db.delete_table('footprint_configentity')

        # Removing M2M table for field categories on 'ConfigEntity'
        db.delete_table('footprint_configentity_categories')

        # Removing M2M table for field built_form_sets on 'ConfigEntity'
        db.delete_table('footprint_configentity_built_form_sets')

        # Removing M2M table for field policy_sets on 'ConfigEntity'
        db.delete_table('footprint_configentity_policy_sets')

        # Removing M2M table for field media on 'ConfigEntity'
        db.delete_table('footprint_configentity_media')

        # Deleting model 'TemplateEnergyWaterFeature'
        db.delete_table('footprint_templateenergywaterfeature')

        # Deleting model 'Job'
        db.delete_table('footprint_job')

        # Deleting model 'TemplateBaseFeature'
        db.delete_table('footprint_templatebasefeature')

        # Deleting model 'TemplateDevelopableFeature'
        db.delete_table('footprint_templatedevelopablefeature')

        # Deleting model 'PresentationMedium'
        db.delete_table('footprint_presentationmedium')

        # Removing M2M table for field tags on 'PresentationMedium'
        db.delete_table('footprint_presentationmedium_tags')

        # Deleting model 'Layer'
        db.delete_table('footprint_layer')

        # Deleting model 'TemplateScenarioBuiltFormFeature'
        db.delete_table('footprint_templatescenariobuiltformfeature')

        # Deleting model 'PrimaryComponent'
        db.delete_table('footprint_primarycomponent')

        # Deleting model 'PlacetypeComponentCategory'
        db.delete_table('footprint_placetypecomponentcategory')

        # Deleting model 'PlacetypeComponent'
        db.delete_table('footprint_placetypecomponent')

        # Deleting model 'StreetAttributeSet'
        db.delete_table('footprint_streetattributeset')

        # Deleting model 'Placetype'
        db.delete_table('footprint_placetype')

        # Deleting model 'FlatBuiltForm'
        db.delete_table('footprint_flatbuiltform')

        # Deleting model 'Core'
        db.delete_table('footprint_core')

        # Deleting model 'PrimaryComponentPercent'
        db.delete_table('footprint_primarycomponentpercent')

        # Deleting model 'PlacetypeComponentPercent'
        db.delete_table('footprint_placetypecomponentpercent')

        # Deleting model 'GlobalConfig'
        db.delete_table('footprint_globalconfig')

        # Deleting model 'Region'
        db.delete_table('footprint_region')

        # Deleting model 'Project'
        db.delete_table('footprint_project')

        # Deleting model 'Scenario'
        db.delete_table('footprint_scenario')

        # Deleting model 'BaseScenario'
        db.delete_table('footprint_basescenario')

        # Deleting model 'FutureScenario'
        db.delete_table('footprint_futurescenario')

        # Deleting model 'Parcel'
        db.delete_table('footprint_parcel')

        # Deleting model 'GridCell'
        db.delete_table('footprint_gridcell')

        # Deleting model 'Taz'
        db.delete_table('footprint_taz')

        # Deleting model 'Result'
        db.delete_table('footprint_result')

        # Deleting model 'Chart'
        db.delete_table('footprint_chart')

        # Deleting model 'GeoLibrary'
        db.delete_table('footprint_geolibrary')

        # Deleting model 'GeoLibraryCatalog'
        db.delete_table('footprint_geolibrarycatalog')

        # Deleting model 'Grid'
        db.delete_table('footprint_grid')

        # Deleting model 'LayerChart'
        db.delete_table('footprint_layerchart')

        # Deleting model 'Presentation'
        db.delete_table('footprint_presentation')

        # Deleting model 'LayerLibrary'
        db.delete_table('footprint_layerlibrary')

        # Deleting model 'Map'
        db.delete_table('footprint_map')

        # Deleting model 'Painting'
        db.delete_table('footprint_painting')

        # Deleting model 'Report'
        db.delete_table('footprint_report')

        # Deleting model 'ResultLibrary'
        db.delete_table('footprint_resultlibrary')

        # Removing M2M table for field results on 'ResultLibrary'
        db.delete_table('footprint_resultlibrary_results')

        # Deleting model 'Style'
        db.delete_table('footprint_style')

        # Deleting model 'Template'
        db.delete_table('footprint_template')

        # Deleting model 'PresentationConfiguration'
        db.delete_table('footprint_presentationconfiguration')

        # Deleting model 'SortType'
        db.delete_table('footprint_sorttype')

        # Deleting model 'TileStacheConfig'
        db.delete_table('footprint_tilestacheconfig')

        # Deleting model 'SacogLandUseDefinition'
        db.delete_table('footprint_sacoglandusedefinition')

        # Deleting model 'SacogLandUse'
        db.delete_table('footprint_sacoglanduse')

        # Deleting model 'ScagLandUseDefinition'
        db.delete_table('footprint_scaglandusedefinition')

        # Deleting model 'ScagLandUse'
        db.delete_table('footprint_scaglanduse')

        # Deleting model 'DemoLandUseDefinition'
        db.delete_table('footprint_demolandusedefinition')

        # Deleting model 'DemoLandUse'
        db.delete_table('footprint_demolanduse')


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
        'footprint.basescenario': {
            'Meta': {'object_name': 'BaseScenario', '_ormbases': ['footprint.Scenario']},
            'scenario_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.Scenario']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.buildingattributeset': {
            'Meta': {'object_name': 'BuildingAttributeSet'},
            'building_uses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.BuildingUseDefinition']", 'through': "orm['footprint.BuildingUsePercent']", 'symmetrical': 'False'}),
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
        'footprint.buildingusedefinition': {
            'Meta': {'object_name': 'BuildingUseDefinition'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.BuildingUseDefinition']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'footprint.buildingusepercent': {
            'Meta': {'object_name': 'BuildingUsePercent'},
            'building_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.BuildingAttributeSet']"}),
            'building_use_definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.BuildingUseDefinition']"}),
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
        'footprint.builtform': {
            'Meta': {'object_name': 'BuiltForm'},
            'building_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.BuildingAttributeSet']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'examples': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.BuiltFormExample']", 'null': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'built_form_media'", 'symmetrical': 'False', 'to': "orm['footprint.Medium']"}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.Medium']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'origin_built_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.BuiltForm']", 'null': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.Tag']", 'symmetrical': 'False'})
        },
        'footprint.builtformexample': {
            'Meta': {'object_name': 'BuiltFormExample'},
            'content': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'footprint.builtformset': {
            'Meta': {'object_name': 'BuiltFormSet'},
            'built_forms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.BuiltForm']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'footprint.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'footprint.chart': {
            'Meta': {'object_name': 'Chart', '_ormbases': ['footprint.Result']},
            'result_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.Result']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.configentity': {
            'Meta': {'object_name': 'ConfigEntity'},
            'bounds': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'built_form_sets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.BuiltFormSet']", 'symmetrical': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.Category']", 'symmetrical': 'False'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'db_entities': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.DbEntity']", 'through': "orm['footprint.DbEntityInterest']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.Medium']", 'null': 'True', 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'origin_config_entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clone_set'", 'null': 'True', 'to': "orm['footprint.ConfigEntity']"}),
            'parent_config_entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_set'", 'null': 'True', 'to': "orm['footprint.ConfigEntity']"}),
            'policy_sets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.PolicySet']", 'symmetrical': 'False'}),
            'scope': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'selections': ('picklefield.fields.PickledObjectField', [], {'default': "{'db_entities': {}, 'sets': {}}"})
        },
        'footprint.core': {
            'Meta': {'object_name': 'Core'},
            'celery_task': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'completed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'config_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.ConfigEntity']"}),
            'failed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'previous_celery_task': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'started': ('django.db.models.fields.DateField', [], {'null': 'True'})
        },
        'footprint.dbentity': {
            'Meta': {'object_name': 'DbEntity'},
            'class_key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'group_by': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'hosts': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'query': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'schema': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'table': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.Tag']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'})
        },
        'footprint.dbentityinterest': {
            'Meta': {'object_name': 'DbEntityInterest'},
            'config_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.ConfigEntity']"}),
            'db_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.DbEntity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.Interest']"})
        },
        'footprint.demolanduse': {
            'Meta': {'object_name': 'DemoLandUse'},
            'builtform_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.BuiltForm']", 'unique': 'True', 'primary_key': 'True'}),
            'land_use_definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.DemoLandUseDefinition']"})
        },
        'footprint.demolandusedefinition': {
            'Meta': {'object_name': 'DemoLandUseDefinition'},
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
        'footprint.flatbuiltform': {
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
            'dwelling_unit_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'education_services_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'employment_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'extraction_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'gross_net_ratio': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '10'}),
            'household_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'industrial_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'intersection_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
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
            'transport_warehouse_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'}),
            'wholesale_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '10'})
        },
        'footprint.futurescenario': {
            'Meta': {'object_name': 'FutureScenario', '_ormbases': ['footprint.Scenario']},
            'scenario_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.Scenario']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.geography': {
            'Meta': {'object_name': 'Geography'},
            'geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_id': ('django.db.models.fields.TextField', [], {'max_length': '200', 'db_index': 'True'})
        },
        'footprint.geolibrary': {
            'Meta': {'object_name': 'GeoLibrary'},
            'entities': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.DbEntity']", 'through': "orm['footprint.GeoLibraryCatalog']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'footprint.geolibrarycatalog': {
            'Meta': {'object_name': 'GeoLibraryCatalog'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.DbEntity']"}),
            'geo_library': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.GeoLibrary']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {})
        },
        'footprint.globalconfig': {
            'Meta': {'object_name': 'GlobalConfig', '_ormbases': ['footprint.ConfigEntity']},
            'configentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.ConfigEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.grid': {
            'Meta': {'object_name': 'Grid', '_ormbases': ['footprint.Result']},
            'result_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.Result']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.gridcell': {
            'Meta': {'object_name': 'GridCell', '_ormbases': ['footprint.Geography']},
            'geography_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.Geography']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.interest': {
            'Meta': {'object_name': 'Interest'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'})
        },
        'footprint.job': {
            'Meta': {'ordering': "['-created_on']", 'object_name': 'Job'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True'}),
            'ended_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'hashid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobs'", 'to': "orm['auth.User']"})
        },
        'footprint.layer': {
            'Meta': {'object_name': 'Layer', '_ormbases': ['footprint.PresentationMedium']},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'presentationmedium_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.PresentationMedium']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.layerchart': {
            'Meta': {'object_name': 'LayerChart', '_ormbases': ['footprint.Chart']},
            'chart_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.Chart']", 'unique': 'True', 'primary_key': 'True'}),
            'layer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.Layer']"})
        },
        'footprint.layerlibrary': {
            'Meta': {'object_name': 'LayerLibrary', '_ormbases': ['footprint.Presentation']},
            'presentation_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.Presentation']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.map': {
            'Meta': {'object_name': 'Map', '_ormbases': ['footprint.Presentation']},
            'presentation_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.Presentation']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.medium': {
            'Meta': {'object_name': 'Medium'},
            'content': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'footprint.painting': {
            'Meta': {'object_name': 'Painting', '_ormbases': ['footprint.Map']},
            'map_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.Map']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.parcel': {
            'Meta': {'object_name': 'Parcel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'geography': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.Geography']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'wkb_geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {})
        },
        'footprint.placetype': {
            'Meta': {'object_name': 'Placetype', '_ormbases': ['footprint.BuiltForm']},
            'builtform_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.BuiltForm']", 'unique': 'True', 'primary_key': 'True'}),
            'intersection_density': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '4'}),
            'placetype_components': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.PlacetypeComponent']", 'through': "orm['footprint.PlacetypeComponentPercent']", 'symmetrical': 'False'}),
            'street_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.StreetAttributeSet']", 'null': 'True'})
        },
        'footprint.placetypecomponent': {
            'Meta': {'object_name': 'PlacetypeComponent', '_ormbases': ['footprint.BuiltForm']},
            'builtform_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.BuiltForm']", 'unique': 'True', 'primary_key': 'True'}),
            'component_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.PlacetypeComponentCategory']"}),
            'primary_components': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.PrimaryComponent']", 'through': "orm['footprint.PrimaryComponentPercent']", 'symmetrical': 'False'})
        },
        'footprint.placetypecomponentcategory': {
            'Meta': {'object_name': 'PlacetypeComponentCategory'},
            'contributes_to_net': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'footprint.placetypecomponentpercent': {
            'Meta': {'object_name': 'PlacetypeComponentPercent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '21', 'decimal_places': '20'}),
            'placetype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.Placetype']"}),
            'placetype_component': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.PlacetypeComponent']", 'null': 'True'})
        },
        'footprint.policy': {
            'Meta': {'object_name': 'Policy'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'policies': ('django.db.models.fields.related.ManyToManyField', [], {'default': '[]', 'to': "orm['footprint.Policy']", 'symmetrical': 'False'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.Tag']", 'symmetrical': 'False'}),
            'values': ('picklefield.fields.PickledObjectField', [], {})
        },
        'footprint.policyset': {
            'Meta': {'object_name': 'PolicySet'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'policies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.Policy']", 'symmetrical': 'False'})
        },
        'footprint.presentation': {
            'Meta': {'object_name': 'Presentation'},
            'config_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.ConfigEntity']"}),
            'configuration': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.Medium']", 'through': "orm['footprint.PresentationMedium']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'scope': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'footprint.presentationconfiguration': {
            'Meta': {'object_name': 'PresentationConfiguration'},
            'data': ('picklefield.fields.PickledObjectField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'scope': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'footprint.presentationmedium': {
            'Meta': {'object_name': 'PresentationMedium'},
            'configuration': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'db_entity_key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.Medium']"}),
            'medium_context': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'presentation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.Presentation']"}),
            'rendered_medium': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.Tag']", 'symmetrical': 'False'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'visible_attributes': ('picklefield.fields.PickledObjectField', [], {'null': 'True'})
        },
        'footprint.primarycomponent': {
            'Meta': {'object_name': 'PrimaryComponent', '_ormbases': ['footprint.BuiltForm']},
            'builtform_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.BuiltForm']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.primarycomponentpercent': {
            'Meta': {'object_name': 'PrimaryComponentPercent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '21', 'decimal_places': '20'}),
            'placetype_component': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.PlacetypeComponent']"}),
            'primary_component': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.PrimaryComponent']"})
        },
        'footprint.project': {
            'Meta': {'object_name': 'Project', '_ormbases': ['footprint.ConfigEntity']},
            'base_year': ('django.db.models.fields.IntegerField', [], {'default': '2005'}),
            'configentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.ConfigEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.region': {
            'Meta': {'object_name': 'Region', '_ormbases': ['footprint.ConfigEntity']},
            'configentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.ConfigEntity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.report': {
            'Meta': {'object_name': 'Report', '_ormbases': ['footprint.Presentation']},
            'presentation_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.Presentation']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.result': {
            'Meta': {'object_name': 'Result', '_ormbases': ['footprint.PresentationMedium']},
            'presentationmedium_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.PresentationMedium']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.resultlibrary': {
            'Meta': {'object_name': 'ResultLibrary', '_ormbases': ['footprint.Presentation']},
            'presentation_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.Presentation']", 'unique': 'True', 'primary_key': 'True'}),
            'results': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['footprint.Result']", 'symmetrical': 'False'})
        },
        'footprint.sacoglanduse': {
            'Meta': {'object_name': 'SacogLandUse'},
            'builtform_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.BuiltForm']", 'unique': 'True', 'primary_key': 'True'}),
            'land_use_definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.SacogLandUseDefinition']"})
        },
        'footprint.sacoglandusedefinition': {
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
        'footprint.scaglanduse': {
            'Meta': {'object_name': 'ScagLandUse'},
            'builtform_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.BuiltForm']", 'unique': 'True', 'primary_key': 'True'}),
            'land_use_definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.ScagLandUseDefinition']"})
        },
        'footprint.scaglandusedefinition': {
            'Meta': {'object_name': 'ScagLandUseDefinition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_use': ('django.db.models.fields.IntegerField', [], {}),
            'land_use_description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'land_use_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'footprint.scenario': {
            'Meta': {'object_name': 'Scenario', '_ormbases': ['footprint.ConfigEntity']},
            'configentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.ConfigEntity']", 'unique': 'True', 'primary_key': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'footprint.sorttype': {
            'Meta': {'object_name': 'SortType'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order_by': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'unique': 'True', 'null': 'True'})
        },
        'footprint.streetattributeset': {
            'Meta': {'object_name': 'StreetAttributeSet'},
            'block_size': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lane_width': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '4'}),
            'number_of_lanes': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '4'})
        },
        'footprint.style': {
            'Meta': {'object_name': 'Style'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.TextField', [], {}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'style_property': ('django.db.models.fields.TextField', [], {}),
            'target': ('django.db.models.fields.TextField', [], {})
        },
        'footprint.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'footprint.taz': {
            'Meta': {'object_name': 'Taz', '_ormbases': ['footprint.Geography']},
            'geography_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.Geography']", 'unique': 'True', 'primary_key': 'True'})
        },
        'footprint.template': {
            'Meta': {'object_name': 'Template', '_ormbases': ['footprint.Medium']},
            'medium_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['footprint.Medium']", 'unique': 'True', 'primary_key': 'True'}),
            'template_context': ('picklefield.fields.PickledObjectField', [], {})
        },
        'footprint.templatebasefeature': {
            'Meta': {'object_name': 'TemplateBaseFeature'},
            'acres_gross': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_ag': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_ind': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_military': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_mixed': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_off': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_ret': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_mixed': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_mixed_no_off': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_mixed_w_off': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_no_use': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_attsf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_detsf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_detsf_ll': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_detsf_sl': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_mf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_accommodation': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_arts_entertainment': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_attsf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_detsf_ll': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_detsf_sl': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_education': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_medical_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_mf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_office_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_other_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_public_admin': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_restaurant': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_retail_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_transport_warehousing': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_wholesale': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'built_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.BuiltForm']", 'null': 'True', 'blank': 'True'}),
            'commercial_irrigated_sqft': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'du': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_attsf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_detsf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_detsf_ll': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_detsf_sl': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_mf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_mf2to4': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_mf5p': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_occupancy_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_accommodation': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_ag': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_agriculture': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_arts_entertainment': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_construction': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_education': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_extraction': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_ind': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_manufacturing': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_medical_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_military': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_off': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_office_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_other_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_public_admin': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_restaurant': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_ret': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_retail_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_transport_warehousing': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_utilities': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_wholesale': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'geography': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.Geography']", 'null': 'True'}),
            'hh': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_agg_inc': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_avg_inc': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_avg_size': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_avg_vehicles': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_00_10': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_100_125': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_10_20': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_125_150': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_150_200': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_200p': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_20_30': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_30_40': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_40_50': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_50_60': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_60_75': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_75_100': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_owner_occ': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_rental_occ': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intersection_density_sqmi': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'land_development_category': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'landtype': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'pop': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'pop_age16_up': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'pop_age20_64': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'pop_age25_up': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'pop_age65_up': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'pop_avg_age20_64': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'pop_college_degree': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'pop_employed': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'pop_female': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'pop_female_age20_64': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'pop_graduate_degree': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'pop_hs_diploma': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'pop_hs_not_comp': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'pop_male': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'pop_male_age20_64': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'pop_some_college': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'region_lu_code': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'residential_irrigated_sqft': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'sqft_parcel': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'wkb_geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {})
        },
        'footprint.templatecoreendstatefeature': {
            'Meta': {'object_name': 'TemplateCoreEndStateFeature'},
            'acres_gross': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_ag': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_ind': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_military': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_off': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_ret': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_mixed': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_mixed_no_off': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_mixed_w_off': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_no_use': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_attsf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_detsf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_detsf_ll': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_detsf_sl': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_mf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_accommodation': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_arts_entertainment': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_attsf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_detsf_ll': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_detsf_sl': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_education': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_medical_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_mf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_office_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_other_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_public_admin': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_restaurant': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_retail_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_transport_warehousing': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_wholesale': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'built_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.BuiltForm']", 'null': 'True'}),
            'commercial_irrigated_sqft': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'du': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_attsf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_detsf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_detsf_ll': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_detsf_sl': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_mf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_accommodation': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_ag': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_agriculture': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_arts_entertainment': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_construction': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_education': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_extraction': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_ind': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_manufacturing': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_medical_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_military': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_off': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_office_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_other_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_public_admin': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_restaurant': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_ret': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_retail_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_transport_warehousing': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_utilities': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_wholesale': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'geography': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.Geography']", 'null': 'True'}),
            'hh': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pop': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'residential_irrigated_sqft': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'wkb_geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {})
        },
        'footprint.templatecoreincrementfeature': {
            'Meta': {'object_name': 'TemplateCoreIncrementFeature'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'du': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'du_attsf': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'du_detsf': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'du_detsf_ll': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'du_detsf_sl': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'du_mf': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_accommodation': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_ag': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_agriculture': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_arts_entertainment': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_construction': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_education': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_extraction': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_ind': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_manufacturing': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_medical_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_military': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_off': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_office_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_other_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_public_admin': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_restaurant': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_ret': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_retail_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_transport_warehousing': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_utilities': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_wholesale': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'geography': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.Geography']", 'null': 'True'}),
            'hh': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pop': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'refill': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'wkb_geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {})
        },
        'footprint.templatedevelopablefeature': {
            'Meta': {'object_name': 'TemplateDevelopableFeature'},
            'acres_constrained': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_developable': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_greenfield': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_gross': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_ag': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_ind': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_military': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_mixed': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_off': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_ret': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_mixed': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_mixed_no_off': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_mixed_w_off': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_no_use': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_attsf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_detsf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_detsf_ll': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_detsf_sl': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_mf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'acres_urban': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_accommodation': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_arts_entertainment': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_attsf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_detsf_ll': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_detsf_sl': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_education': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_medical_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_mf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_office_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_other_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_public_admin': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_restaurant': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_retail_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_transport_warehousing': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_wholesale': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'commercial_irrigated_sqft': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'du': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_attsf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_detsf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_detsf_ll': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_detsf_sl': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'du_mf': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_accommodation': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_ag': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_agriculture': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_arts_entertainment': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_construction': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_education': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_extraction': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_ind': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_manufacturing': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_medical_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_military': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_off': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_office_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_other_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_public_admin': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_restaurant': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_ret': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_retail_services': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_transport_warehousing': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_utilities': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'emp_wholesale': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'geography': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.Geography']", 'null': 'True'}),
            'hh': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_agg_inc': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_00_10': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_100_125': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_10_20': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_125_150': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_150_200': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_200p': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_20_30': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_30_40': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_40_50': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_50_60': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_60_75': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_inc_75_100': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_owner_occ': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'hh_rental_occ': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pop': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'residential_irrigated_sqft': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'wkb_geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {})
        },
        'footprint.templateenergywaterfeature': {
            'ComEnrgyNewConst': ('django.db.models.fields.DecimalField', [], {'default': '30', 'max_digits': '5', 'decimal_places': '2'}),
            'ComEnrgyReplcmt': ('django.db.models.fields.DecimalField', [], {'default': '1.0', 'max_digits': '3', 'decimal_places': '2'}),
            'ComEnrgyRetro': ('django.db.models.fields.DecimalField', [], {'default': '0.8', 'max_digits': '3', 'decimal_places': '2'}),
            'ComIndWatrNewConst': ('django.db.models.fields.DecimalField', [], {'default': '30', 'max_digits': '5', 'decimal_places': '2'}),
            'ComIndWatrReplcmt': ('django.db.models.fields.DecimalField', [], {'default': '0.2', 'max_digits': '3', 'decimal_places': '2'}),
            'ComIndWatrRetro': ('django.db.models.fields.DecimalField', [], {'default': '0.08', 'max_digits': '3', 'decimal_places': '2'}),
            'Meta': {'object_name': 'TemplateEnergyWaterFeature'},
            'ResEnrgyNewConst': ('django.db.models.fields.DecimalField', [], {'default': '30', 'max_digits': '5', 'decimal_places': '2'}),
            'ResEnrgyReplcmt': ('django.db.models.fields.DecimalField', [], {'default': '0.6', 'max_digits': '3', 'decimal_places': '2'}),
            'ResEnrgyRetro': ('django.db.models.fields.DecimalField', [], {'default': '0.5', 'max_digits': '3', 'decimal_places': '2'}),
            'ResWatrNewConst': ('django.db.models.fields.DecimalField', [], {'default': '30', 'max_digits': '5', 'decimal_places': '2'}),
            'ResWatrReplcmt': ('django.db.models.fields.DecimalField', [], {'default': '0.06', 'max_digits': '3', 'decimal_places': '2'}),
            'ResWatrRetro': ('django.db.models.fields.DecimalField', [], {'default': '0.05', 'max_digits': '3', 'decimal_places': '2'}),
            'Water_GPCD_MF': ('django.db.models.fields.IntegerField', [], {'default': '70'}),
            'Water_GPCD_SF': ('django.db.models.fields.IntegerField', [], {'default': '80'}),
            'Water_GPED_Industrial': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'Water_GPED_Office': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'Water_GPED_Retail': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'Water_GPED_School': ('django.db.models.fields.IntegerField', [], {'default': '86'}),
            'ann_ind_elec_peremp': ('django.db.models.fields.FloatField', [], {'default': '27675.45'}),
            'ann_ind_gas_peremp': ('django.db.models.fields.FloatField', [], {'default': '767.56'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'geography': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.Geography']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'wkb_geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {})
        },
        'footprint.templatescenariobuiltformfeature': {
            'Meta': {'object_name': 'TemplateScenarioBuiltFormFeature'},
            'acres_developable': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_developing': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_gross': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_ag': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_ind': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_mixed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_off': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_emp_ret': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_mixed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_mixed_no_off': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_mixed_w_off': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_attsf': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_detsf_ll': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_detsf_sl': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'acres_parcel_res_mf': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_accommodation': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_arts_entertainment': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_attsf': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_detsf_ll': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_detsf_sl': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_education': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_medical_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_mf': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_office_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_other_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_public_admin': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_restaurant': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_retail_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_transport_warehousing': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'bldg_sqft_wholesale': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'built_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.BuiltForm']", 'null': 'True'}),
            'commercial_irrigated_sqft': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'density_pct': ('django.db.models.fields.DecimalField', [], {'default': '1.0', 'max_digits': '8', 'decimal_places': '4'}),
            'dev_pct': ('django.db.models.fields.DecimalField', [], {'default': '1.0', 'max_digits': '8', 'decimal_places': '4'}),
            'dirty_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'du': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'du_attsf': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'du_detsf_ll': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'du_detsf_sl': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'du_mf': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_accommodation': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_ag': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_agriculture': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_arts_entertainment': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_construction_utilities': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_education': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_extraction': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_ind': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_manufacturing': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_medical_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_military': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_off': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_office_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_other_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_public_admin': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_restaurant': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_ret': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_retail_services': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_transport_warehousing': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'emp_wholesale': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'geography': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['footprint.Geography']", 'null': 'True'}),
            'hh': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pop': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'refill_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'residential_irrigated_sqft': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '4'}),
            'total_redev': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'wkb_geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {})
        },
        'footprint.tilestacheconfig': {
            'Meta': {'object_name': 'TileStacheConfig'},
            'config': ('picklefield.fields.PickledObjectField', [], {}),
            'enable_caching': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '50'})
        }
    }

    complete_apps = ['footprint']