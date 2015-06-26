#!/usr/bin/env python

"""
Retrieves tweets and mashes up with geojson for camps where possible

Refer to https://dev.twitter.com/overview/api/tweets for status/tweet object field guide
Refer to https://dev.twitter.com/rest/public/rate-limits for rate limits
"""

import twitter
import ConfigParser
import simplejson as json
import time
from datetime import datetime


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
tweets_json = [] 
for t in tweets:	
	tweets_json.append({ 
		"created_at": t.created_at, 		
		"coordinates": t.coordinates, 
		"id": t.id, 		
		"text": t.text  })
timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
f = open("tweets-%s.json" % timestamp,'w')
json.dump(tweets_json,f,indent=4, sort_keys=True)
f.close()