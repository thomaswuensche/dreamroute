import googlemaps
import credentials
import logging as log
import pprint
import sys
from datetime import datetime

pp = pprint.PrettyPrinter(indent=2)

log.basicConfig(level=log.INFO,
    format='%(levelname)s : %(funcName)s @ %(lineno)s - %(message)s')

gmaps = googlemaps.Client(key=credentials.apikey)

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("HTW Berlin Wilhelminenhof",
    "HTW Berlin Treskowallee",
    mode="transit",
    departure_time=now)

log.info('transit')
log.info(directions_result[0]['legs'][0]['distance']['text'])
log.info(directions_result[0]['legs'][0]['duration']['text'])

# Request directions via bike
now = datetime.now()
directions_result = gmaps.directions("HTW Berlin Wilhelminenhof",
    "HTW Berlin Treskowallee",
    mode="bicycling",
    departure_time=now)

log.info('bike')
log.info(directions_result[0]['legs'][0]['distance']['text'])
log.info(directions_result[0]['legs'][0]['duration']['text'])

# Request directions by foot
now = datetime.now()
directions_result = gmaps.directions("HTW Berlin Wilhelminenhof",
    "HTW Berlin Treskowallee",
    mode="walking",
    departure_time=now)

log.info('walking')
log.info(directions_result[0]['legs'][0]['distance']['text'])
log.info(directions_result[0]['legs'][0]['duration']['text'])
