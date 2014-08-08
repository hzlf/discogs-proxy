# -*- coding: utf-8 -*-
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import logging

log = logging.getLogger(__name__)

from dgsauth.settings import USER_AGENT_STRING
from dgsauth.settings import API_KEY
from dgsauth.settings import API_SECRET
from dgsauth.settings import API_ACCESS_TOKEN
from dgsauth.settings import API_ACCESS_SECRET

REQUEST_TOKEN_URL = 'http://api.discogs.com/oauth/request_token'
BASE_AUTHORIZE_URL = 'http://www.discogs.com/oauth/authorize'
ACCESS_TOKEN_URL = 'http://api.discogs.com/oauth/access_token'
USER_IDENTITY_URL = 'http://api.discogs.com/oauth/identity'

class DiscogsOAuthException(Exception):
    pass


class DiscogsOAuth(object):

    def __init__(self,
                 api_key=API_KEY,
                 api_secret=API_SECRET,
                 access_token=API_ACCESS_TOKEN,
                 access_secret=API_ACCESS_SECRET):

        if not (api_key and api_secret):
            raise DiscogsOAuthException('api_key and api_secret are required!')

        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_secret = access_secret

        self.api_username = None
        self.api_user_id = None

        if access_token and access_secret:
            self.auth = OAuth1(self.api_key,
                               client_secret=self.api_secret,
                               resource_owner_key=self.access_token,
                               resource_owner_secret=self.access_secret)
        else:
            self.auth = OAuth1(self.api_key, client_secret=self.api_secret)

        self.request_headers = {
            'User-Agent': USER_AGENT_STRING
        }

        log.debug('api_key: %s' % api_key)
        log.debug('api_secret: %s' % api_secret)
        log.debug('access_token: %s' % access_token)
        log.debug('access_secret: %s' % access_secret)
        log.debug('User-Agent: %s' % USER_AGENT_STRING)


    def start_authorization(self):

        return self.get_request_token()


    def get_request_token(self):

        log.debug('Requesting request-tokens')

        r = requests.post(REQUEST_TOKEN_URL, auth=self.auth, headers=self.request_headers)

        if not r.status_code == 200:
            raise DiscogsOAuthException('Server error: %s - "%s"' % (r.status_code, r.text))

        try:
            credentials = parse_qs(r.content)
            owner_key = credentials.get('oauth_token')[0]
            owner_secret = credentials.get('oauth_token_secret')[0]

            log.info('Got OAuth - token: %s secret: %s' % (owner_key, owner_secret))

        except Exception, e:
            raise DiscogsOAuthException('Unable to extract credentials' % e)


        if owner_key and owner_secret:
            return self.get_authorization(owner_key, owner_secret)


    def get_authorization(self, owner_key, owner_secret):

        log.debug('Requesting authorization')

        if not (owner_key and owner_secret):
            raise DiscogsOAuthException('owner_key and/or owner_secret missing')

        authorize_url = '%s?oauth_token=%s' % (BASE_AUTHORIZE_URL, owner_key)

        print
        print
        print 'Open the url \n%s\nin your browser, click on "Authorize" and enter the displayed "code" below' % authorize_url

        verifier = raw_input('Input the code from the website: ')

        print "*%s*" % verifier

        return self.get_access_token(owner_key, owner_secret, verifier)


    def get_access_token(self, owner_key, owner_secret, verifier):

        log.debug('Requesting access-tokens')

        print 'api_key: %s' % self.api_key
        print 'api_secret: %s' % self.api_secret
        print 'owner_key: %s' % owner_key
        print 'owner_key: %s' % owner_secret
        print 'verifier: %s' % verifier

        auth = OAuth1(self.api_key,
                      client_secret=self.api_secret,
                      resource_owner_key=owner_key,
                      resource_owner_secret=owner_secret,
                      verifier=verifier)

        r = requests.post(url=ACCESS_TOKEN_URL, auth=auth, headers=self.request_headers)

        if not r.status_code == 200:
            raise DiscogsOAuthException('Server error: %s - "%s"' % (r.status_code, r.text))

        try:
            credentials = parse_qs(r.content)
            access_token = credentials.get('oauth_token')[0]
            access_secret = credentials.get('oauth_token_secret')[0]

            log.info('Got OAuth - access_token: %s access_secret: %s' \
                     % (access_token, access_secret))

            if not (access_token and access_secret):
                raise DiscogsOAuthException('Unable to extract credentials')

        except Exception, e:
            raise DiscogsOAuthException('Unable to extract credentials' % e)

        self.access_token = access_token
        self.access_secret = access_secret

        # recreate auth object
        self.auth = OAuth1(self.api_key,
                           client_secret=self.api_secret,
                           resource_owner_key=self.access_token,
                           resource_owner_secret=self.access_secret)

        return True


    def authorize(self):

        log.debug('Trying to authorize in Discogs API')

        r = requests.get(url=USER_IDENTITY_URL, auth=self.auth, headers=self.request_headers)

        identity = r.json()

        try:
            self.api_username = identity['username']
            self.api_user_id = identity['id']

            log.info('Successfully authorized: %s  - (id: %s)' \
                     % (self.api_username, self.api_user_id))

            return True

        except Exception, e:
            log.warning('Unable to authorize : %s' % e)

            return False

