# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Draft'
        db.create_table('draft_draft', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, blank=True)),
            ('serialized_data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('draft', ['Draft'])


    def backwards(self, orm):
        
        # Deleting model 'Draft'
        db.delete_table('draft_draft')


    models = {
        'draft.draft': {
            'Meta': {'object_name': 'Draft'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'serialized_data': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['draft']
