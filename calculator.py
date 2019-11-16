from data_handler import DataHandler

class Calculator():

    def __init__(self, gmaps, connection):
        self.gmaps = gmaps
        self.connection = connection

    def calculate_trip(self, start, destination, departure, mobility_type, model):
        directions_result = self.gmaps.directions(start,
            destination,
            mobility_type,
            departure_time=departure)

        # log.info(mobility_type)
        # log.info(directions_result[0]['legs'][0]['distance']['text'])
        # log.info(directions_result[0]['legs'][0]['duration']['text'])

        distance = directions_result[0]['legs'][0]['distance']['value']
        duration = directions_result[0]['legs'][0]['duration']['value']

        data = DataHandler(self.connection)

        emissions = data.get_emissions(mobility_type, model)
        emissions_on_trip = round(emissions*(distance/1000), 2)
        # log.info('CO2 emissions: {}kg'.format(emissions_on_trip))

        price = data.get_price(mobility_type, model)
        if price['min'] == True:
            price_of_trip = round(price['value']*(duration/60), 2)
        else:
            price_of_trip = round(price['value']*(distance/1000), 2)
        # log.info('Price of trip: {}€'.format(price_of_trip))

        return (distance, duration)
