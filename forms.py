from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField

class SearchForm(FlaskForm):
    start =StringField('Start', validators=[DataRequired()])
    destination = StringField('Destination', validators=[DataRequired()])
    departure_date = DateField('Departure Date', format='%Y-%m-%d', validators=[DataRequired()])
    departure_time = TimeField('Departure Time', validators=[DataRequired()])
    mobility_types = SelectMultipleField('Select mobility type', default='transit', choices=[('transit', 'transit'), ('bicycling', 'bicycling'), ('walking', 'walking'), ('driving', 'driving')])
    submit = SubmitField('Go')


