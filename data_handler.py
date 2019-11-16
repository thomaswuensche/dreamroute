class DataHandler():

    def __init__(self, connection):
        self.connection = connection

    def get_emissions(self, mobility_type, model):
        cursor = self.connection.cursor()
        sql = "SELECT emissions_per_km FROM emissions WHERE mobility_type=%(mobility_type)s"

        if model:
            sql = sql + " AND model='{}'".format(model)

        val = {'mobility_type': mobility_type}

        cursor.execute(sql, val)
        for result in cursor:
            emissions = result[0]

        cursor.close()
        return emissions

    def get_price(self, mobility_type, model):
        cursor = self.connection.cursor()
        sql = "SELECT price_per_km, price_per_min FROM emissions WHERE mobility_type=%(mobility_type)s"

        if model:
            sql = sql + " AND model='{}'".format(model)

        val = {'mobility_type': mobility_type}

        cursor.execute(sql, val)
        for result in cursor:
            if result[0]:
                price = result[0]
                min = False
            else:
                price = result[1]
                min = True

        cursor.close()
        return {'value': price, 'min' : min}
