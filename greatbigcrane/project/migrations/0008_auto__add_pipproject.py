# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PipProject'
        db.create_table('project_pipproject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['project.Project'], unique=True)),
            ('virtualenv_path', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('test_command', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('project', ['PipProject'])


    def backwards(self, orm):
        
        # Deleting model 'PipProject'
        db.delete_table('project_pipproject')


    models = {
        'project.pipproject': {
            'Meta': {'object_name': 'PipProject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['project.Project']", 'unique': 'True'}),
            'test_command': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'virtualenv_path': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
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
