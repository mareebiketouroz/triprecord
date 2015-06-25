"""
Retrieves SPOT gps check in messages from a gmail folder
and outputs in a kml file
"""

import imaplib
import simplekml

kml = simplekml.Kml()

## set these
email = ''
pass = ''
folder = 'SPOT'
outputfile = 'camps.kml'

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
    kml.newpoint(name=date, coords=[(lon,lat)]) # kml marker
mail.close()
mail.logout()
kml.save(outputfile)
print 'Camps kml written to %s' % outputfile
