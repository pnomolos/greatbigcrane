# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Project.project_type'
        db.add_column('project_project', 'project_type', self.gf('django.db.models.fields.CharField')(default='buildout', max_length=9), keep_default=False)

        # Changing field 'Project.description'
        db.alter_column('project_project', 'description', self.gf('django.db.models.fields.TextField')(blank=True))


    def backwards(self, orm):
        
        # Deleting field 'Project.project_type'
        db.delete_column('project_project', 'project_type')

        # Changing field 'Project.description'
        db.alter_column('project_project', 'description', self.gf('django.db.models.fields.TextField')())


    models = {
        'project.project': {
            'Meta': {'object_name': 'Project'},
            'base_directory': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'favourite': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'git_repo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'project_type': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'test_status': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['project']
