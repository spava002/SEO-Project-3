'''
This form should collect user data on preference of school
Data should be: 
    residency (In-State or Out-of-State) --> String type
    school_type (Public or Private) --> String type
    program (Name of desired program if any) --> String type
    degree (Name of desired degree) --> String type
    tuition_preference (Desired tuition if specified) --> int type
    room_preference (Desired room pricing if specified) --> int type
'''
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, AnyOf, ValidationError
from us_states_territories import us_states_territories


# Modified AnyOf() method to be case in-sensitive
class CaseInsensitiveAnyOf(AnyOf):
    def __call__(self, form, field):
        field.data = field.data.lower()
        if field.data not in self.values:
            message = self.message
            if message is None:
                message = field.gettext("Invalid US state or territory.")
            raise ValidationError(message)
    

class SchoolForm(FlaskForm):
    # Required parameters
    degree = StringField('Degree: ', validators=[DataRequired(), Length(min=3, max=50, message='Invalid degree. Must be between 3-50 characters.')], render_kw={"autocomplete": "off"})
    degree_type = SelectField("Degree Type: ", validators=[Optional()], choices=[(None, "None"), ("Associate's Degree", "Associate's Degree"), ("Bachelor's Degree", "Bachelor's Degree"), ("Master's Degree", "Master's Degree"), ("Doctoral Degree", "Doctorate (Ph.D.) Degree")], render_kw={"autocomplete": "off"})
    residency = StringField('Current State or Territory You Reside In: ', validators=[DataRequired(), CaseInsensitiveAnyOf(us_states_territories)], render_kw={"autocomplete": "off"})
    residency_preference = SelectField('In-State or Out-Of-State: ', validators=[DataRequired()], choices=[("instate", "In-State"), ("outofstate", "Out-Of-State")], render_kw={"autocomplete": "off"})
    # Optional parameters
    school_type = SelectField('Public or Private: ', validators=[Optional()], choices=[("public", "Public"), ("private", "Private")], render_kw={"autocomplete": "off"})
    tuition_preference = SelectField('Tuition Preference: ', validators=[Optional()], choices=[(None, "None"), (1000, "$0-$1,000"), (5000, "$0-$5,000"), (10000, "$0-$10,000"), (20000, "$0-$20000"), (30000, "$0-$30,000"), (40000, "$0-$40,000")], render_kw={"autocomplete": "off"})
    # Submit data
    submit = SubmitField('Search')
