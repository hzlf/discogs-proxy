# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CachedFile'
        db.create_table(u'dgsproxy_cachedfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
        ))
        db.send_create_signal(u'dgsproxy', ['CachedFile'])


    def backwards(self, orm):
        # Deleting model 'CachedFile'
        db.delete_table(u'dgsproxy_cachedfile')


    models = {
        u'dgsproxy.cachedfile': {
            'Meta': {'object_name': 'CachedFile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['dgsproxy']