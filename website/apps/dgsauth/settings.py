"""Settings of Discogs AUTH"""
from django.conf import settings

from dgsauth import __version__, __url__

USER_AGENT_STRING = getattr(settings, 'DGSAUTH_USER_AGENT_STRING',
                            'PBIDiscogsAuth/%s - %s' % (__version__, __url__))

# API credentials
API_KEY = getattr(settings, 'DGSAUTH_API_KEY', None)
API_SECRET = getattr(settings, 'DGSAUTH_API_SECRET', None)
API_ACCESS_TOKEN = getattr(settings, 'DGSAUTH_API_ACCESS_TOKEN', None)
API_ACCESS_SECRET = getattr(settings, 'DGSAUTH_API_ACCESS_SECRET', None)
