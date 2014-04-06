from flask_oauth import OAuth
from flask import session
import flask.ext.login
import os

class TwitterOAuth (object):
    oauth = None
    twitter_auth = None

    def __init__(self, twitter_key=None, twitter_secret=None):
        self.oauth = OAuth()
        if not twitter_key or not twitter_secret:
            twitter_key, twitter_secret =  self.__get_auth_keys()
        self.twitter_auth = self.oauth.remote_app('twitter',
            base_url='https://api.twitter.com/1/',
            request_token_url='https://api.twitter.com/oauth/request_token',
            access_token_url='https://api.twitter.com/oauth/access_token',
            authorize_url='https://api.twitter.com/oauth/authenticate',
            consumer_key=twitter_key,
            consumer_secret=twitter_secret
        )

    def __get_auth_keys(self):
        twitter_key = None
        twitter_secret = None
        try: # try getting creds from ifle
            with open('twittercreds.txt') as creds:
                c = [x for x in creds]
                twitter_key = c[0]
                twitter_secret = c[1]
        except:
            pass # Ok try envvars

        try:
            twitter_key = os.environ['TWITTER_ACCESS_KEY']
            twitter_secret = os.environ['TWITTER_SECRET_KEY']
        except:
            pass

        if twitter_key is None or twitter_secret is None:
            raise Exception("You must define twitter API credentials.")

        return (twitter_key, twitter_secret)
