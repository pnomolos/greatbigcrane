# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Project.updated_at'
        db.add_column('project_project', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.date.today(), blank=True), keep_default=False)

        # Adding field 'Project.created_at'
        db.add_column('project_project', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.date.today(), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Project.updated_at'
        db.delete_column('project_project', 'updated_at')

        # Deleting field 'Project.created_at'
        db.delete_column('project_project', 'created_at')


    models = {
        'project.project': {
            'Meta': {'object_name': 'Project'},
            'base_directory': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'git_repo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['project']
