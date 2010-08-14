# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Notification'
        db.create_table('notifications_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('notifications', ['Notification'])


    def backwards(self, orm):
        
        # Deleting model 'Notification'
        db.delete_table('notifications_notification')


    models = {
        'notifications.notification': {
            'Meta': {'object_name': 'Notification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['notifications']
