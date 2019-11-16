import googlemaps
import credentials
import logging as log
import pprint
import mysql.connector as mysql
import argparse
import sys
from datetime import datetime

pp = pprint.PrettyPrinter(indent=2)

log.basicConfig(level=log.DEBUG,
    format='%(levelname)s : %(funcName)s @ %(lineno)s - %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--start', help='starting location', required=True)
parser.add_argument('-d', '--destination', help='destination', required=True)
parser.add_argument('-m', '--mobility-type', help='mode you want to travel with',
    required=True, choices=['transit', 'bycycling', 'walking', 'driving'])
args = parser.parse_args()

gmaps = googlemaps.Client(key=credentials.apikey)

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions(args.start,
    args.destination,
    args.mobility_type,
    departure_time=now)

log.info(args.mobility_type)
log.info(directions_result[0]['legs'][0]['distance']['text'])
log.info(directions_result[0]['legs'][0]['duration']['text'])

distance = directions_result[0]['legs'][0]['distance']['value']

connection = mysql.connect(user=credentials.user,
    password=credentials.password,
    host=credentials.host,
    database=credentials.database)
log.debug('connection opened')

cursor = connection.cursor()
sql = "SELECT emissions_per_m FROM emissions WHERE mobility_type=%(mobility_type)s"
val = {'mobility_type': args.mobility_type}

cursor.execute(sql, val)
for result in cursor:
    emissions = result[0]

cursor.close()

emissions_on_trip = round(emissions*distance, 2)
log.info('CO2 emissions in kg: {}'.format(emissions_on_trip))
