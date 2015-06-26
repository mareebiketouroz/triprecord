# triprecord

Trip record includes utilities to gather information about a trip and display it on a map

It is a work in progress.

Make changes to blank.config and save as my.config

This assumes you are using gmail and you have your spot gps sending emails to your account, and you have set up a filter to deliver these messages to a particular folder.

* get_spot_messages_from_gmail_kml.py produces a kml file with name set to date of each point. This can be imported with Google My Maps.

* get_spot_messages_from_gmail_geojson.py produces a geojson file (feature collection) with feature property "date" set to date. This can be displayed as a layer with leaflet.js

* tweets_geojson.py produces a geojson file (feature collection) with feature property "date" set to date and "tweets" set to tweets sent the same day

## Todo

* location tweets mapped
* location photos mapped
* tweets or photos not georeferrenced assigned to the camp lat/lon as a daily summary
* leaflet map showing camps and tweets for that day
* google my maps pointing at cloud kml