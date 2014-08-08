from django.contrib import admin

from models import CachedResource

class CachedResourceAdmin(admin.ModelAdmin):

    list_display = ['__unicode__',  'created', 'content_type', 'filesize', 'status']
    list_filter = ['content_type', 'status']
    date_hierarchy = 'created'

admin.site.register(CachedResource, CachedResourceAdmin)