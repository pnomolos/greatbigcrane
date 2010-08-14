# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Preference'
        db.create_table('preferences_preference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('preferences', ['Preference'])


    def backwards(self, orm):
        
        # Deleting model 'Preference'
        db.delete_table('preferences_preference')


    models = {
        'preferences.preference': {
            'Meta': {'object_name': 'Preference'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['preferences']
