# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DbEntity.origin_instance'
        db.add_column('main_dbentity', 'origin_instance',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.DbEntity'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'DbEntity.origin_instance'
        db.delete_column('main_dbentity', 'origin_instance_id')


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
            'origin_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.DbEntity']", 'null': 'True'}),
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
            'origin_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Layer']", 'null': 'True'}),
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