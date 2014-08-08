# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CachedResource.uri_md5'
        db.add_column(u'dgsproxy_cachedresource', 'uri_md5',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CachedResource.uri_md5'
        db.delete_column(u'dgsproxy_cachedresource', 'uri_md5')


    models = {
        'dgsproxy.cachedresource': {
            'Meta': {'object_name': 'CachedResource'},
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '56', 'null': 'True', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'db_index': 'True'}),
            'uri_md5': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['dgsproxy']