from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from filteredForm import SchoolForm
from unfilteredForm import SchoolNameForm
from singleSchoolData import main
import git
import logging


app = Flask(__name__)
app.config['SECRET_KEY'] = 'PS7T6txPuOaXKkNnvToX90e0J'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schools.db'

db = SQLAlchemy(app)


class Schools(db.Model):
    # id, degree, and residency will always contain a value
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(50), nullable=False)
    residency = db.Column(db.String(50), nullable=False)
    residency_preference = db.Column(db.String(50), nullable=False)
    # school_type, tuition_preference, and room_preference won't always contain a value
    school_type = db.Column(db.String(50), nullable=False)
    tuition_preference = db.Column(db.Integer, nullable=False)
    room_preference = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return ""

with app.app_context():
    db.create_all()

# Functionality to support website when hosted on pythonanywhere.com

# @app.route("/update_server", methods=['POST'])
# def webhook():
#     if request.method == 'POST':
#         repo = git.Repo('/home/spava001/SEO-Project-2-NEW')
#         origin = repo.remotes.origin
#         origin.pull()
#         return 'Updated PythonAnywhere successfully', 200
#     else:
#         return 'Wrong event type', 400

# Route for home page
@app.route("/", methods=['POST', 'GET'])
def renderHome():
    filteredForm = SchoolForm()
    unfilteredForm = SchoolNameForm()
    if filteredForm.validate_on_submit():
        '''
        This portion was meant for testing purposes
        '''
        # degree = filteredForm.degree.data
        # residency = filteredForm.residency.data
        # residency_preference = filteredForm.residency_preference.data
        # school_type = filteredForm.school_type.data
        # tuition_preference = filteredForm.tuition_preference.data
        # room_preference = filteredForm.room_preference.data
        # main(degree, residency, residency_preference, school_type, tuition_preference, room_preference)
        return redirect(url_for('renderSearchResults', data="The filtered form was submitted!"))
    elif unfilteredForm.validate_on_submit():
        school_name = unfilteredForm.school_name.data
        main(school_name)
        return redirect(url_for('renderSearchResults', data="The unfiltered form was submitted!"))
    
    return render_template('home.html', filteredForm=filteredForm, unfilteredForm=unfilteredForm)


# Route for search results 
@app.route("/search-results", methods=['GET'])
def renderSearchResults():
    data = request.args.get('data')
    return render_template('searchResults.html', data=data)


# Route for chosen college
@app.route("/college", methods=['GET'])
def renderChoseCollege():
    return render_template('college.html')


# Route for a database page (meant for testing purposes)
@app.route("/db")
def renderDb():
    all_school_data = Schools.query.all()
    return render_template('db.html', all_school_data=all_school_data)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")