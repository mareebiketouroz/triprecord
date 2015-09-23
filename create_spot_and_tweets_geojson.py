#!/usr/bin/env python

"""
Retrieves tweets and spot messages and mashes up spot camps markers with tweets for the same day, outputs as geojson

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

## libraries to get oembed from twitter
import requests
from requests_oauthlib import OAuth1


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
tweets = api.GetUserTimeline(user, count=maxtweets, include_rts=False) 
tweets_json = {}
format_created_at = "ddd MMM DD HH:mm:ss Z YYYY"
format_date = "YYYY-MM-DD"
oembed_auth = OAuth1(consumerkey,consumersecret,accesstokenkey,accesstokensecret)
for t in tweets:
	d = arrow.get(t.created_at, format_created_at).format(format_date)

	## get oembed html
	url = "https://api.twitter.com/1.1/statuses/oembed.json?omit_script=true&id=%s" % t.id
	r = requests.get(url,auth=oembed_auth)
	data = r.json()
	embed = data['html']


	if d not in tweets_json:
		tweets_json[d] = []
	tweets_json[d].append({ 
		"time": arrow.get(t.created_at, format_created_at).format('HH:mm'),
		"created_at": t.created_at, 		
		#"coordinates": t.coordinates, 
		"id": t.id, 		
		"text": t.text,
		"embed": embed })
timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
f = open("tweets-%s.json" % timestamp,'w')
json.dump(tweets_json,f,indent=4, sort_keys=True)
f.close()
"""
Retrieves SPOT gps check in messages from a gmail folder
and outputs in a geojson file

Note: if you have two step verification, you should use a
app password instead of your usual password. See https://support.google.com/accounts/answer/185833?hl=en and https://security.google.com/settings/security/apppasswords?pli=1 for more information
"""

import imaplib
import geojson
import ConfigParser
from dateutil import parser

config =  ConfigParser.ConfigParser()
config.read('my.config')

## set these
email = config.get('email','email')
passwd = config.get('email', 'passwd')
folder = config.get('email', 'folder')
outputfile = config.get('output', 'geojsonfile')
spotdatetimeformat = config.get('spot','datetimeformat')
isodatetimeformat = config.get('misc','isodatetimeformat')

features = []

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(email, passwd) 
mail.select(folder) 
typ, data = mail.search(None, 'ALL')
for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)')
    lat=None
    lon=None
    date=None
    msg = data[0][1]
    lines = msg.split('\n')
    for line in lines:
        line = line.strip()
        if line.find('Latitude:') != -1 and line.find('X-SPOT') == -1:
            lat = float(line.replace('Latitude:',''))
        if line.find('Longitude:') != -1 and line.find('X-SPOT') == -1:
            lon = float(line.replace('Longitude:',''))
        if line.find('GPS location Date/Time:') != -1:
            date = line.replace('GPS location Date/Time:','')
    if lat and lon and date:
        print "Lat %s Lon %s Date %s" % (lat, lon, date)
        date = parser.parse(date).strftime(isodatetimeformat)
	## get tweets for date
	d = arrow.get(date).format('YYYY-MM-DD')
	t = []
	if d in tweets_json:
	    t = tweets_json[d]	
        feature = geojson.Feature(geometry=geojson.Point((lon,lat)), properties={"date": date, "tweets": t})
        features.append(feature)
    else:
        print "Lat/lon/date not found"
mail.close()
mail.logout()

if len(features) > 0:
    featurecollection = geojson.FeatureCollection(features)
    f = open(outputfile,'w')
    geojson.dump(featurecollection, f, indent=4)
    f.close()
    print 'Camps geojson saved to %s' % outputfile
else:
    print 'No features found'

