#!/usr/bin/env python

"""
Retrieves SPOT gps check in messages from a gmail folder
and outputs in a kml file
"""

import imaplib
import simplekml
import datetime
from dateutil import parser

kml = simplekml.Kml()

import ConfigParser

config =  ConfigParser.ConfigParser()
config.read('my.config')

## set these
email = config.get('email','email')
passwd = config.get('email', 'passwd')
folder = config.get('email', 'folder')
outputfile = config.get('output', 'kmlfile')
spotdatetimeformat = config.get('spot','datetimeformat')
isodatetimeformat = config.get('misc','isodatetimeformat')

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(email, passwd) 
mail.select(folder) 
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
    date = parser.parse(date).strftime(isodatetimeformat)    
    kml.newpoint(name=date, coords=[(lon,lat)]) # kml marker
mail.close()
mail.logout()
kml.save(outputfile)
print('Camps kml written to {}'.format(outputfile))
