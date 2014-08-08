Discogs OAuth & caching proxy
=============================

A rather quick implementation of an auth-proxy for discogs.

The `discogs API <http://www.discogs.com/developers/>`_ requires authentication to access image
resources `since february 2014 <http://www.discogs.com/forum/thread/52950c194c5e2e7adca760a0>`_,
the search endpoint will require authentication
from `from august 15th 2014 <http://www.discogs.com/forum/thread/521520689469733cfcfd2089>`_ as well.

It is totally understandable that discogs introduce these limits to identify trouble-making
applications and abusing/badly implemented clients!

We did build this proxy to be able to serve our legacy apps without having to re-implement the
discogs API-calls. (These apps are mainly web-based and for internal use, and only generate a
verry limited amount of requests.)

Using this proxy, we only need to change the url used in the legacy-clients to access the discogs
API. (which is, obviously, http://api.discogs.com/)

All API-calls then land on the proxy, the proxy adds the credentials/user-agent and sends the
request to discogs. As an additional benefit, the responses can be cached - so requesting the same
image multiple times, or firing the same search-query subsequently only needs to stress the
discogs-infrastructure once!


Further the proxy rewrites the *resource_url*s - these are rewritten to the proxies *SITE_URL*.



The proxy is implemented in python/django - and basically involves two modules:

- **dgsauth** which handles the credentials
- **dgsproxy** which handles the requests

The **dgsauth** module is built in a way that allows stand-alone usage (in django) and is built
on top of `python-requests <http://docs.python-requests.org/>`_. It basically helps to go through
the OAuth-flow, and can provide an *auth-instance* to be used at other places.



Installation
------------

System requirements
:::::::::::::::::::

*nix system, providing the basics needed to work with/run python/django

It is assumed that you use *pip* and *virtualenv* - it could be installed and used in other ways as well...


Application
:::::::::::

Code & requirements
"""""""""""""""""""

.. code-block::

    git clone https://github.com/hzlf/discogs-proxy.git && cd discogs-proxy

    virtualenv env
    source env/bin/activate

    pip install -r website/requirements/requirements.txt




Basic settings & database
"""""""""""""""""""""""""

The example settings include a configuration for sqlite, you should probably configure postgres or mysql here.
Tough it likely will run fine with sqlite as well if you don't expect heavy usage...

.. code-block::

    cd website

    cp project/example_local_settings.py project/local_settings.py
    nano project/local_settings.py

    ./manage.py syncdb --all
    ./manage.py migrate --fake

    ./manage.py runserver 0.0.0.0:8000


Please check now if you can access the backend at http://localhost:8000/admin/



Aquiring OAuth credentials
""""""""""""""""""""""""""

The **dgsauth** module provides you with a convenient management_command get the needed credentials.

First you have to get an account and configure an app on discogs. Visit
https://www.discogs.com/settings/developers and creat an application. For the next step you need to know your

- "Consumer Key" and
- "Consumer Secret"

Equipped with these information, proceed with the dgsauth management-command:


.. code-block::

    ./manage.py dgsauth_setup

Follow the instruction provided by the command, at the end you will be provided with the information needed to configure your settings. It will look something like:

.. code-block:: pycon

    DGSAUTH_API_KEY = "HGEcvqUTDVlDnsRaVIeF"
    DGSAUTH_API_SECRET = "BErQSpGWqXMgHYQDwBHAOGliajHCFSQv"
    DGSAUTH_API_ACCESS_TOKEN = "ybYsyfvLwXcSIRIhBzxGLFxBMRroxGLkCpdIzZnQ"
    DGSAUTH_API_ACCESS_SECRET = "lrPvDJPLprUVBJVUluVipmVUfmUuEahbTDFTyjlH"

Add these settings to the *project/local_settings.py* - DONE!


Test your installation
""""""""""""""""""""""

.. code-block::

    ./manage.py runserver 0.0.0.0:8000

and access an API resource, like

- http://localhost:8000/image/R-35292-1332501840.jpeg
- http://localhost:8000/releases/266364 (this EP is from me b.t.w :) )
- http://localhost:8000/database/search?q=madonna (this EP is from me b.t.w :) )

This is extremely alpha and just here for 'fun' - but there are minimal statistics displayed at
http://localhost:8000/

(note that the statistics only work if configure a cache backend, the defauld *LocMemCache*
backend does not work correctly here because of threading)



Deployment
::::::::::

I'll not cover here the topics regarding django-deployment. Preferences and needs differ, and likely
you have your 'own way' here...

Just remember, DON'T run this proxy on a public server without further steps!!

It could be just fine to deploy it internally (say: internal network), using *supervisord* or a
similar tool to control the process. (this is what we do...)

There are plans to add a little nginx config-example, but not really with high priority...
Anyway, suggestons and improvements are warmly welcome!!


Deployment for legacy applications
""""""""""""""""""""""""""""""""""

There are dozens of scenarios on how to implement these kind of proxies, here just one use-case
(the one here...):

to not having touch legacy-code at all, you could setup the proxy-app inside
(or on a server anywhere) and just add a dns entry in your site(s) internet-gateway
that points *api.discogs.com* to the proxy instance...



Settings
::::::::

TODO



dgsauth settings
""""""""""""""""

- DGSAUTH_USER_AGENT_STRING
- DGSAUTH_API_KEY
- DGSAUTH_API_SECRET
- DGSAUTH_API_ACCESS_TOKEN
- DGSAUTH_API_ACCESS_SECRET


dgsproxy settings
""""""""""""""""

- SITE_URL
- DGSPROXY_USER_AGENT_STRING
- DGSPROXY_CACHE_DIRECTORY
- DGSPROXY_HASH_CACHE
- DGSPROXY_HASH_SPLIT
- DGSPROXY_CACHE_DURATION
- DGSPROXY_CLEAR_CACHE_ON_SAVE







