'''
This form should collect user data on preference of school
Data should be: 
    residency (In-State or Out-of-Stae) --> String type
    school_type (Public or Private) --> String type
    program (Name of desired program if any) --> String type
    degree (Name of desired degree) --> String type
    tuition_preference (Desired tuition if specified) --> int type
    room_preference (Desired room pricing if specified) --> int type
'''
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, AnyOf


# Modified AnyOf() method to be case in-sensitive
class CaseInsensitiveAnyOf(AnyOf):
    def __call__(self, form, field):
        field.data = field.data.lower()
        super().__call__(form, field)


class SchoolForm(FlaskForm):
    # Required parameters
    degree = StringField('Degree: ', validators=[DataRequired(), Length(min=3, max=50, message='Invalid degree. Must be between 3-50 characters.')], render_kw={"autocomplete": "off"})
    residency = SelectField('In-State or Out-Of-State: ', validators=[DataRequired()], choices=[("instate", "In-State"), ("outofstate", "Out-Of-State")], render_kw={"autocomplete": "off"})
    # Optional parameters
    school_type = SelectField('In-State or Out-Of-State: ', validators=[Optional()], choices=[("public", "Public"), ("private", "Private")], render_kw={"autocomplete": "off"})
    tuition_preference = SelectField('Tuition Preference: ', validators=[Optional()], choices=[("0-10000", "$0-$10,000"), ("0-20000", "$0-$20,000"), ("0-30000", "$0-$30,000"), ("0-40000", "$0-$40,000"), ("0-50000", "$0-$50,000")], render_kw={"autocomplete": "off"})
    room_preference = SelectField('Room Preference: ', validators=[Optional()], choices=[("0-10000", "$0-$10,000"), ("0-20000", "$0-$20,000"), ("0-30000", "$0-$30,000"), ("0-40000", "$0-$40,000"), ("0-50000", "$0-$50,000")], render_kw={"autocomplete": "off"})
    # Submit data
    submit = SubmitField('Search')
