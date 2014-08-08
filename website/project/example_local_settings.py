import os
from project.settings import *

gettext = lambda s: s
_ = gettext

COMPRESS_ENABLED = True
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*',]


"""
IMPORTANT!
Site running the proxy (incl. protocol & port)
value will be used to rewrite api results!
"""
SITE_URL = 'http://localhost:8000/'


"""
API credentials, run
./manage.py dgsauth_setup
to get them
"""

#DGSAUTH_API_KEY = ""
#DGSAUTH_API_SECRET = ""
#DGSAUTH_API_ACCESS_TOKEN = ""
#DGSAUTH_API_ACCESS_SECRET = ""


"""
Discogs proxy settings
"""
DGSPROXY_CACHE_DURATION = 600

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = '*****************************'


"""
Preferably postgres or mysql for production
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data.sqlite3'),
    },
}


"""
Optional. Cache is only required to display statistics.
"""
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'dgsproxy',
    }
}

