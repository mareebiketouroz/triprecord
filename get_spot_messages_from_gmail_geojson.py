#!/usr/bin/env python

"""
Retrieves SPOT gps check in messages from a gmail folder
and outputs in a geojson file

Note: if you have two step verification, you should use a
app password instead of your usual password. See https://support.google.com/accounts/answer/185833?hl=en and https://security.google.com/settings/security/apppasswords?pli=1 for more information
"""

import imaplib
import geojson
import ConfigParser

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
        feature = geojson.Feature(geometry=geojson.Point((lon,lat)), properties={"date": date})
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

