# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Notification.summary'
        db.add_column('notifications_notification', 'summary', self.gf('django.db.models.fields.CharField')(default='', max_length=128), keep_default=False)

        # Adding field 'Notification.notification_time'
        db.add_column('notifications_notification', 'notification_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2010, 8, 14, 13, 30, 36, 607074), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Notification.summary'
        db.delete_column('notifications_notification', 'summary')

        # Deleting field 'Notification.notification_time'
        db.delete_column('notifications_notification', 'notification_time')


    models = {
        'notifications.notification': {
            'Meta': {'object_name': 'Notification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'notification_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['notifications']
