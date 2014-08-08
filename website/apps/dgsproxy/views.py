# -*- coding: utf-8 -*-
import hashlib
import datetime
import logging
import json

from django.http import HttpResponse
from django.views.generic import View

from dgsproxy.models import CachedResource
from dgsproxy.stats import ProxyStats, set_hit

log = logging.getLogger(__name__)

class ResourceView(View):

    def get(self, *args, **kwargs):

        type = kwargs.get('type', None)
        uri = kwargs.get('uri', None)

        try:
            query_string = self.request.META['QUERY_STRING']
            if len(query_string):
                uri = '%s?%s' % (uri, query_string)
        except Exception, e:
            query_string = None

        log.debug('Requesting: %s - %s' % (type, uri))

        #CachedResource.objects.all().delete()

        #resource, created = CachedResource.objects.get_or_create(type=type, uri=uri)

        resource, created = CachedResource.objects.get_or_create(type=type, uri_md5=hashlib.md5(uri).hexdigest())
        resource.uri = uri
        set_hit('backend' if created else 'cache')

        path = resource.get_file_path()

        if path:
            with open(path, "rb") as f:

                response = HttpResponse(f.read(), content_type=resource.content_type)
                response['Last-Modified'] = resource.updated.strftime('%a, %d %b %Y %H:%M:%S GMT')
                return response

        response = HttpResponse('file not found', status=404)
        response['Last-Modified'] = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response


class StatsView(View):

    def get(self, *args, **kwargs):

        stats = ProxyStats()

        response = HttpResponse(json.dumps(stats.get_stats()), content_type="application/json")

        return response

