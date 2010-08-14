# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'Preference', fields ['name']
        db.create_unique('preferences_preference', ['name'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Preference', fields ['name']
        db.delete_unique('preferences_preference', ['name'])


    models = {
        'preferences.preference': {
            'Meta': {'object_name': 'Preference'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['preferences']
