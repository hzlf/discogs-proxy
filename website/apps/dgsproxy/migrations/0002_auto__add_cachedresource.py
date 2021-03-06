# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CachedResource'
        db.create_table(u'dgsproxy_cachedresource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=56, null=True, db_index=True)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, db_index=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=512, null=True)),
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'dgsproxy', ['CachedResource'])


    def backwards(self, orm):
        # Deleting model 'CachedResource'
        db.delete_table(u'dgsproxy_cachedresource')


    models = {
        u'dgsproxy.cachedfile': {
            'Meta': {'object_name': 'CachedFile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        u'dgsproxy.cachedresource': {
            'Meta': {'object_name': 'CachedResource'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '512', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '56', 'null': 'True', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['dgsproxy']