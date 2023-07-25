'''
This form should collect the user's desired user and pass for future logins
Data should be: 
    username (any string at the moment between 3-50 chars is valid) --> string type
    password (any string of atleast 8 characters, one uppercase character, and a number) --> string type
    confirm_password (must match previously entered password) --> string type
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
    

def validatePassword(form, field):
    password = field.data
    if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password):
        raise ValidationError("Password must be 8 characters minimum, include an uppercase character, and a number.")


def confirmPassword(form, field):
    if form.password.data != field.data:
        raise ValidationError("Passwords do not match!")


class signUp(FlaskForm):
    # Required parameters
    username = StringField('Username: ', validators=[DataRequired(), Length(min=3, max=50, message='Invalid username. Must be between 3-20 characters.')], render_kw={"autocomplete": "off"})
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=3, max=50), validatePassword])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), Length(min=3, max=50), confirmPassword])
    # Submit data
    submit = SubmitField('Sign Up')