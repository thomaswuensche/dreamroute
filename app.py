from flask import Flask, render_template, request
from datetime import date, datetime, timedelta
from forms import SearchForm
import credentials
from test import get_routeinfo


app = Flask(__name__)

app.config['SECRET_KEY'] = credentials.secretKey


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
        route_infos = []
        for mobility_type in mobility_types:
            route_infos.append(get_routeinfo(start, destination, departure, mobility_type))
            
        
        return render_template('index.html', form=form, start=start, destination=destination, departure_date=departure_date, departure_time=departure_time, departure=departure, mobility_types=mobility_types, route_infos = route_infos )
    return render_template('index.html', form=form)
        

if __name__ == '__main__':
    app.run()