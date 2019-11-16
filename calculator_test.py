import googlemaps
import credentials
import logging as log
import pprint
import mysql.connector as mysql
import argparse
import sys
from data_handler import DataHandler
from datetime import datetime

pp = pprint.PrettyPrinter(indent=2)

log.basicConfig(level=log.DEBUG,
    format='%(levelname)s : %(funcName)s @ %(lineno)s - %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--start', help='starting location', required=True)
parser.add_argument('-d', '--destination', help='destination', required=True)
parser.add_argument('-m', '--model', help='model')
parser.add_argument('-t', '--mobility-type', help='mode you want to travel with',
    required=True, choices=['transit', 'bycycling', 'walking', 'driving'])
args = parser.parse_args()

gmaps = googlemaps.Client(key=credentials.apikey)

directions_result = gmaps.directions(args.start,
    args.destination,
    args.mobility_type,
    departure_time=datetime.now())

log.info(args.mobility_type)
log.info(directions_result[0]['legs'][0]['distance']['text'])
log.info(directions_result[0]['legs'][0]['duration']['text'])

distance = directions_result[0]['legs'][0]['distance']['value']
duration = directions_result[0]['legs'][0]['duration']['value']

connection = mysql.connect(user=credentials.user,
    password=credentials.password,
    host=credentials.host,
    database=credentials.database)
log.debug('connection opened')

data = DataHandler(connection)

emissions = data.get_emissions(args.mobility_type, args.model)
emissions_on_trip = round(emissions*(distance/1000), 2)
log.info('CO2 emissions in kg: {}'.format(emissions_on_trip))

price = data.get_price(args.mobility_type, args.model)
if price['min'] == True:
    price_of_trip = price['value']*(duration/60)
else:
    price_of_trip = price['value']*(distance/1000)
log.info('Price of trip: {}'.format(price_of_trip))
