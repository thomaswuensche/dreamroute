from flask import Flask, render_template, request
from datetime import date, datetime, timedelta
from forms import SearchForm
import credentials
import googlemaps
import logging as log
import mysql.connector as mysql
from calculator import Calculator
import sys

app = Flask(__name__)

app.config['SECRET_KEY'] = credentials.secretKey

log.basicConfig(level=log.DEBUG,
    format='%(levelname)s : %(funcName)s @ %(lineno)s - %(message)s')

gmaps = googlemaps.Client(key=credentials.apikey)
connection = mysql.connect(user=credentials.user,
    password=credentials.password,
    host=credentials.host,
    database=credentials.database)

calculator = Calculator(gmaps, connection)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if request.method == 'GET':
        form.departure_date.data = date.today()
        form.departure_time.data = datetime.now()
    if form.is_submitted():
        start = form.start.data
        destination = form.destination.data
        departure_date = form.departure_date.data
        departure_time = form.departure_time.data
        departure = datetime.combine(departure_date,departure_time)
        mobility_types = form.mobility_types.data
        model = form.model.data
        route_infos = []
        for mobility_type in mobility_types:
            route_infos.append(calculator.calculate_trip(start, destination, departure, mobility_type, model))

        return render_template('index.html', form=form, start=start, destination=destination,
            departure=departure, route_infos=route_infos)

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run()
