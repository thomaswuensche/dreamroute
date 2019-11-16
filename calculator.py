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

        distance = directions_result[0]['legs'][0]['distance']['value']
        distance_km = round(distance/1000, 2)

        duration = directions_result[0]['legs'][0]['duration']['value']
        duration_min = round(duration/60)

        data = DataHandler(self.connection)

        emissions = data.get_emissions(mobility_type, model)
        emissions_on_trip = round(emissions*(distance/1000), 2)

        price = data.get_price(mobility_type, model)
        if price['min'] == True:
            price_of_trip = round(price['value']*(duration/60), 2)
        else:
            price_of_trip = round(price['value']*(distance/1000), 2)

        return {
            'mobility_type': mobility_type,
            'distance': distance_km,
            'duration': duration_min,
            'emissions_on_trip': emissions_on_trip,
            'price_of_trip': price_of_trip
        }
