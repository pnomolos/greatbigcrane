# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Preference.help_text'
        db.add_column('preferences_preference', 'help_text', self.gf('django.db.models.fields.CharField')(default='', max_length=512), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Preference.help_text'
        db.delete_column('preferences_preference', 'help_text')


    models = {
        'preferences.preference': {
            'Meta': {'object_name': 'Preference'},
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['preferences']
