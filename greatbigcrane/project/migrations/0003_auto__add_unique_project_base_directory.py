# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'Project', fields ['base_directory']
        db.create_unique('project_project', ['base_directory'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Project', fields ['base_directory']
        db.delete_unique('project_project', ['base_directory'])


    models = {
        'project.project': {
            'Meta': {'object_name': 'Project'},
            'base_directory': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'git_repo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['project']
