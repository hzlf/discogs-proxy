# -*- coding: utf-8 -*-
import os
import sys
import shutil
import hashlib
import magic
import logging
import gzip
from random import randrange
import datetime
import requests

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from dgsproxy.storage import ReplaceFileStorage
from dgsproxy.exceptions import DiscogsFetcException
from dgsauth.auth import DiscogsOAuth
from dgsproxy.stats import set_rate_limit

from dgsproxy.settings import API_BASE_URL
from dgsproxy.settings import REWRITE_RESOURCE_URLS
from dgsproxy.settings import CACHE_DIRECTORY
from dgsproxy.settings import CACHE_DURATION
from dgsproxy.settings import HASH_CACHE
from dgsproxy.settings import HASH_SPLIT
from dgsproxy.settings import CLEAR_CACHE_ON_SAVE
from dgsproxy.settings import USER_AGENT_STRING





log = logging.getLogger(__name__)

INIT = 0
DONE = 1
QUEUED = 2
ERROR = 99
STATUS_CHOICES = (
    (INIT, 'Init'),
    (DONE, 'Done'),
    (QUEUED, 'Queued'),
    (ERROR, 'Error'),
)

def create_upload_path(instance, filename):
    folder = os.path.join(settings.MEDIA_ROOT, CACHE_DIRECTORY)

    if HASH_CACHE:
        hashed_uri = hashlib.md5(instance.uri).hexdigest()
        bits = map(''.join, zip(*[iter(hashed_uri)] * HASH_SPLIT))
        return os.path.join(folder, instance.type, '/'.join(bits))

    else:
        return os.path.join(folder, instance.type, )


class CachedResource(models.Model):
    type = models.CharField(max_length=56, blank=False, null=True, db_index=True)
    uri = models.CharField(max_length=512, blank=False, null=True, db_index=True)
    uri_md5 = models.CharField(max_length=32, blank=False, null=True, db_index=True)
    file = models.FileField(storage=ReplaceFileStorage(), upload_to=create_upload_path,
                            max_length=512, blank=True, null=True)
    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES)
    content_type = models.CharField(max_length=36, blank=True, null=True)
    filesize = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta(object):
        app_label = 'dgsproxy'
        verbose_name = 'Cached Resource'
        verbose_name_plural = 'Cached Resources'

    def __unicode__(self):

        return '%s/%s' % (self.type, self.uri)

    def get_file_path(self):

        if self.file and os.path.exists(self.file.path):
            log.debug('File does exist in local cache: %s' % self.file.path)
            return self.file.path

        else:
            log.debug('File not in cache: %s - will try to fetch from remote API' % self.file)
            return self.get_remote_file()


    def get_remote_file(self):

        log.debug('Get resource from API: %s - %s ' % (self.type, self.uri))

        url = '%s%s/%s' % (API_BASE_URL, self.type, self.uri)
        auth = DiscogsOAuth().auth
        request_headers = { 'User-Agent': USER_AGENT_STRING }

        r = requests.get(url, auth=auth, headers=request_headers)

        if not r.status_code == 200:
            raise DiscogsFetcException('Server error: %s - "%s"' % (r.status_code, r.text))

        content_type = r.headers.get('content-type', None)
        content_length = r.headers.get('content-length', None)

        #
        rate_limit = r.headers.get('x-ratelimit-limit', None)
        rate_limit_remain = r.headers.get('x-ratelimit-remaining', None)

        if rate_limit and rate_limit_remain:
            set_rate_limit(rate_limit, rate_limit_remain)

        if content_type == 'application/json' and REWRITE_RESOURCE_URLS:

            content = u'%s' % r.content
            content = r.content.replace(API_BASE_URL, REWRITE_RESOURCE_URLS)

            f_temp = NamedTemporaryFile(delete=True)
            f_temp.write(content)
            f_temp.flush()

        else:

            f_temp = NamedTemporaryFile(delete=True)
            for chunk in r.iter_content(10):
                f_temp.write(chunk)
            f_temp.flush()

        self.file = File(f_temp, self.uri)
        self.content_type = content_type
        self.filesize = content_length


        self.save()

        return self.file.path



    def save(self, *args, **kwargs):

        # cleanup
        if CLEAR_CACHE_ON_SAVE and randrange(10) == 5:
            clear_outdated_resources()

        super(CachedResource, self).save(*args, **kwargs)


@receiver(post_delete, sender=CachedResource)
def cached_resource_delete(sender, instance, **kwargs):

    if instance.file:
        log.debug('Post delete action, remove file: %s' % instance.file.path)
        instance.file.delete(False)



def clear_outdated_resources(seconds_to_keep=CACHE_DURATION):

    if seconds_to_keep == None:
        return

    log.debug('Clear outdated resources. Cache duration is: %s' % seconds_to_keep)

    clear_date = datetime.datetime.now() - datetime.timedelta(seconds=seconds_to_keep)

    qs = CachedResource.objects.filter(created__lte=clear_date)

    count = qs.count()
    if count > 0:
        log.debug('%s outdated resources to delete' % count)
        qs.delete()

    return count


# TODO: move to util module or similar
def clear_cache_dirs():
    path = os.path.join(settings.MEDIA_ROOT, CACHE_DIRECTORY)
    clear_empty_dirs(path)

def clear_empty_dirs(path):

    if not os.path.isdir(path):
        return

    files = os.listdir(path)
    if len(files):
        for f in files:
            abs_path = os.path.join(path, f)
            if os.path.isdir(abs_path):
                clear_empty_dirs(abs_path)

    files = os.listdir(path)
    if len(files) == 0:
        log.debug('Clearing empty directory: %s' % path)
        os.rmdir(path)
