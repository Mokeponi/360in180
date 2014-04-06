from flask_oauth import OAuth
import os

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
    twitter_secret  os.environ['TWITTER_SECRET_KEY']
except:
    pass

if twitter_key is None or twitter_secret is None:
    raise Exception("You must define twitter API credentials.")


oauth = OAuth()
twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=twitter_key,
    consumer_secret=twitter_secret
)


