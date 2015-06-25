#!/usr/bin/env python

"""
Retrieves SPOT gps check in messages from a gmail folder
and outputs in a geojson file
"""

import imaplib
import geojson 

## set these
email = ''
passwd = ''
folder = 'SPOT' #the folder where the SPOT GPS messages were filtered to
outputfile = 'camps.geojson'

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
	   feature = geojson.Feature(geometry=geojson.Point((lon,lat)), properties={"date": date})
	   features.append(feature)
    else:
        print "Lat/lon/date not found"
mail.close()
mail.logout()

if len(features) > 0:
    featurecollection = geojson.FeatureCollection(features)
    f = open(outputfile,'w')
    geojson.dump(featurecollection, f)
    f.close()
    print 'Camps geojson saved to %s' % outputfile
else:
    print 'No features found'

