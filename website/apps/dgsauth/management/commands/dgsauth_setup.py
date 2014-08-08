# -*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ImproperlyConfigured

from dgsauth.auth import DiscogsOAuth

from dgsauth.settings import USER_AGENT_STRING
from dgsauth.settings import API_KEY
from dgsauth.settings import API_SECRET
from dgsauth.settings import API_ACCESS_TOKEN
from dgsauth.settings import API_ACCESS_SECRET

#if not (API_KEY and API_SECRET):
#    raise ImproperlyConfigured('DGSAUTH_API_KEY and DGSAUTH_API_SECRET are required settings')


class Command(BaseCommand):
    help = 'Step through to get Discogs API credentials'

    option_list = BaseCommand.option_list + (
        make_option('--force',
            action='store_true',
            dest='force_auth',
            default=False,
            help='Force OAuth reset'),
        )

    def handle(self, *args, **options):

        self.stdout.write('Discogs API OAuth flow')
        self.stdout.write('')

        force_authentication = False

        if (API_KEY and API_SECRET and API_ACCESS_TOKEN and API_ACCESS_SECRET) and not force_authentication:

            self.stdout.write('You have already configured API_ACCESS_TOKEN and API_ACCESS_SECRET')
            self.stdout.write('Enter "yes" to reset the API credentials, ')
            self.stdout.write('or hit return to just test the authentication')
            self.stdout.write('')

            force = raw_input('Reset the API credentials (yes/no): ')

            if force == 'yes':
                force_authentication = True



        if (API_KEY and API_SECRET and API_ACCESS_TOKEN and API_ACCESS_SECRET) and not force_authentication:

            dgs_auth = DiscogsOAuth(api_key=API_KEY,
                                    api_secret=API_SECRET,
                                    access_token=API_ACCESS_TOKEN,
                                    access_secret=API_ACCESS_SECRET)

            if dgs_auth.authorize():

                self.stdout.write('')
                self.stdout.write('Successfully authenticated!')
                self.stdout.write('API username: %s' % dgs_auth.api_username)
                self.stdout.write('')
                self.stdout.write('')

            else:
                self.stdout.write('')
                self.stdout.write('Sorry - the authentication failed.')
                self.stdout.write('')
                self.stdout.write('')

        else:

            if not (API_KEY and API_SECRET):
                self.stdout.write('')
                self.stdout.write('')
                self.stdout.write('Ener your API-key & secret - you can get them at:')
                self.stdout.write('https://www.discogs.com/settings/developers')
                self.stdout.write('')

                api_key = raw_input('Consumer Key: ')
                api_secret = raw_input('Consumer Secret: ')

            else:
                api_key = API_KEY
                api_secret = API_SECRET

            dgs_auth = DiscogsOAuth(api_key=api_key,
                                    api_secret=api_secret,
                                    access_token=None,
                                    access_secret=None)

            if dgs_auth.start_authorization():

                self.stdout.write('')
                self.stdout.write('Successfully authenticated!')
                self.stdout.write('API username: %s' % dgs_auth.api_username)

                self.stdout.write('Add the following to your settings:')
                self.stdout.write('')
                self.stdout.write('')
                self.stdout.write('DGSAUTH_API_KEY = "%s"' % dgs_auth.api_key)
                self.stdout.write('DGSAUTH_API_SECRET = "%s"' % dgs_auth.api_secret)
                self.stdout.write('DGSAUTH_API_ACCESS_TOKEN = "%s"' % dgs_auth.access_token)
                self.stdout.write('DGSAUTH_API_ACCESS_SECRET = "%s"' % dgs_auth.access_secret)
                self.stdout.write('')
                self.stdout.write('')


            else:
                self.stdout.write('')
                self.stdout.write('Sorry - the authentication failed.')
                self.stdout.write('')
                self.stdout.write('')


