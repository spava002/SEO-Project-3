'''
This form should only collect the name of a specific school
Data should be: 
    school_name (any string at the moment between 3-50 chars is valid) --> string type
        - In the case an invalid school_name is input, no results will be displayed upon search
'''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, AnyOf
    

class SchoolNameForm(FlaskForm):
    # Required parameters
    school_name = StringField('Search: ', validators=[DataRequired(), Length(min=3, max=50, message='Invalid school name. Must be between 3-50 characters.')], render_kw={"autocomplete": "off"})
    # Submit data
    submit = SubmitField('Search')