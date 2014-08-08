# -*- coding: utf-8 -*-
from decimal import Decimal
import logging
from django.core.cache import cache
from django.db.models import Sum

log = logging.getLogger(__name__)

CACHE_PREFIX = 'dgsproxy_stats_'

class ProxyStats(object):

    def __init__(self):

        self.hits_proxied = 0
        self.hits_cached = 0
        self.num_resources = 0
        self.cache_size = 0
        self.rate_limit = 0
        self.rate_limit_remain = 0


    def build_stats(self):

        # Get values from cache
        self.hits_proxied = cache.get('%s_hits_backend' % CACHE_PREFIX, 0)
        self.hits_cached = cache.get('%s_hits_cache' % CACHE_PREFIX, 0)
        self.rate_limit = cache.get('%s_rate_limt' % CACHE_PREFIX, 0)
        self.rate_limit_remain = cache.get('%s_rate_limt_remain' % CACHE_PREFIX, 0)

        # Get values from db
        from dgsproxy.models import CachedResource
        self.num_resources = CachedResource.objects.count()
        try:
            total_size = int(CachedResource.objects.aggregate(Sum('filesize'))['filesize__sum'])
        except:
            total_size = 0
        self.cache_size = total_size


    def get_stats(self):

        self.build_stats()

        stats = {
            'hits_proxied': self.hits_proxied,
            'hits_cached': self.hits_cached,
            'num_resources': self.num_resources,
            'cache_size': '%.2f' % (float(self.cache_size) / 1024 / 1024),
            'rate_limit': self.rate_limit,
            'rate_limit_remain': self.rate_limit_remain
        }

        return stats


    def set_rate_limit(self, limit, remain):

        pass



def set_rate_limit(limit, remain):

    log.debug('Update rate-limit: %s / %s' % (remain, limit))
    # Write values to cache
    cache.set('%s_rate_limt' % CACHE_PREFIX, int(limit))
    cache.set('%s_rate_limt_remain' % CACHE_PREFIX, int(remain))

    pass

def set_hit(target):

    if target in ('cache', 'backend'):

        log.debug('Add %s hit' % target)

        key = '%s_hits_%s' % (CACHE_PREFIX, target)

        if cache.get(key):
            cache.incr(key)
        else:
            cache.set(key, 1)
