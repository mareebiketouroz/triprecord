"""
Retrieves SPOT gps check in messages from a gmail folder
and outputs in a geojson file
"""

import imaplib
import geojson

## set these
email = ''
pass = ''
folder = 'SPOT'
outputfile = 'camps.geojson'

features = []

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(email, pass) 
mail.select('SPOT') #the folder where the SPOT GPS messages were filtered to
typ, data = mail.search(None, 'ALL')
for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)')
    lat=''
    lon=''
    date=''
    msg = data[0][1]
    lines = msg.split('\n')
    for line in lines:
        line = line.strip()
        if line.find('Latitude:') != -1 and line.find('X-SPOT') == -1:
            lat = line.replace('Latitude:','')
        if line.find('Longitude:') != -1 and line.find('X-SPOT') == -1:
            lon = line.replace('Longitude:','')
        if line.find('GPS location Date/Time:') != -1:
            date = line.replace('GPS location Date/Time:','')
	feature = Feature(geometry=Point((lon,lat)), properties={"date": date})
	features.append(feature)
featurecollection = FeatureCollection(features)
mail.close()
mail.logout()
f = open(outputfile)
geojson.dump(featurecollection, f)
f.close()
print 'Camps geojson saved to %s' % outputfile
