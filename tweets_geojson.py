#!/usr/bin/env python

"""
Retrieves tweets and mashes up with geojson for camps where possible

Refer to https://dev.twitter.com/overview/api/tweets for status/tweet object field guide
Refer to https://dev.twitter.com/rest/public/rate-limits for rate limits

Use pip install python-twitter

Make sure you update your certifi package regularly to get the latest root 
certificates
pip install certifi
See urllib3.readthedocs.org/en/latest/security.html for more info.
"""

import urllib3
import certifi
import twitter
import ConfigParser
import simplejson as json
import time
from datetime import datetime
import arrow

## setup certifi with urllib3
## setup your pool to require a certificate
## and provide the certifi bundle
http = urllib3.PoolManager(
	cert_reqs='CERT_REQUIRED', # Force certificate check
	ca_certs=certifi.where(), # Path to certifi bundle
)

## get settings from my.config
config =  ConfigParser.ConfigParser()
config.read('my.config')
consumerkey=config.get('twitter', 'consumerkey')
consumersecret=config.get('twitter', 'consumersecret')
accesstokenkey=config.get('twitter', 'accesstokenkey')
accesstokensecret=config.get('twitter', 'accesstokensecret')
owner=config.get('twitter', 'owner')
ownerid=config.get('twitter', 'ownerid')
user=config.get('twitter','user')
maxtweets=config.get('twitter','maxtweets')
createdatformat=config.get('twitter', 'createdatformat')

## log in with twitter api to get tweets
api = twitter.Api(
	consumer_key=consumerkey,
	consumer_secret=consumersecret,
        access_token_key=accesstokenkey,
        access_token_secret=accesstokensecret)

#print api.VerifyCredentials()

## "Wed Aug 27 13:08:45 +0000 2008"
#%a %b %d %H:%M:%S %z %Y

## put tweets into our json
tweets = api.GetUserTimeline(user, count=maxtweets) 
tweets_json = {}
format_created_at = "ddd MMM DD HH:mm:ss Z YYYY"
format_date = "YYYY-MM-DD"
for t in tweets:
	d = arrow.get(t.created_at, format_created_at).format(format_date)
	if d not in tweets_json:
		tweets_json[d] = []
	tweets_json[d].append({ 
		"time": arrow.get(t.created_at, format_created_at).format('HH:mm'),
		"created_at": t.created_at, 		
		#"coordinates": t.coordinates, 
		"id": t.id, 		
		"text": t.text  })
timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
f = open("tweets-%s.json" % timestamp,'w')
json.dump(tweets_json,f,indent=4, sort_keys=True)
f.close()
