# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option


class Command(BaseCommand):
    help = 'Clear resource cache. Depends on DGSPROXY_CACHE_DURATION setting.'

    option_list = BaseCommand.option_list + (
        make_option('--all',
            action='store_true',
            dest='clear_all',
            default=False,
            help='Clear all resources (ignores DGSPROXY_CACHE_DURATION)'),
        )

    def handle(self, *args, **options):

        from dgsproxy.models import clear_outdated_resources, clear_cache_dirs

        if options['clear_all']:
            cleared_count = clear_outdated_resources(seconds_to_keep=0)

        else:
            cleared_count = clear_outdated_resources()

        clear_cache_dirs()

        self.stdout.write('Cleaned cache for %s resources.' % cleared_count)