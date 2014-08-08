"""Settings of Discogs proxy"""
from django.conf import settings

from dgsauth import __version__, __url__

USER_AGENT_STRING = getattr(settings, 'DGSPROXY_USER_AGENT_STRING',
                            'PBIDiscogsProxy/%s - %s' % (__version__, __url__))

API_BASE_URL = 'http://api.discogs.com/'
REWRITE_RESOURCE_URLS = getattr(settings, 'SITE_URL', 'http://localhost:8000/')
CACHE_DIRECTORY = getattr(settings, 'DGSPROXY_CACHE_DIRECTORY', 'dgsproxy')
HASH_CACHE = getattr(settings, 'DGSPROXY_HASH_CACHE', True)
HASH_SPLIT = getattr(settings, 'DGSPROXY_HASH_SPLIT', 4)
CACHE_DURATION = getattr(settings, 'DGSPROXY_CACHE_DURATION', 6000)
CLEAR_CACHE_ON_SAVE = getattr(settings, 'DGSPROXY_CLEAR_CACHE_ON_SAVE', False)

