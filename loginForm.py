'''
This form should collect the user's desired user and pass to login
Data should be: 
    username (existing username) --> string type
    password (existiing password to go alongside username) --> string type
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class login(FlaskForm):
    # Required parameters
    username = StringField('Username: ', validators=[DataRequired(), Length(min=3, max=50, message='Invalid username. Must be between 3-20 characters.')], render_kw={"autocomplete": "off"})
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=3, max=50)])
    # Submit data
    submit = SubmitField('Login')