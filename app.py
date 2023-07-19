from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from unfilteredForm import SchoolForm
import git
import logging


app = Flask(__name__)
app.config['SECRET_KEY'] = 'PS7T6txPuOaXKkNnvToX90e0J'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schools.db'

db = SQLAlchemy(app)


class Schools(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    residency = db.Column(db.String(50), nullable=False)
    school_type = db.Column(db.String(50), nullable=False)
    program = db.Column(db.String(50), nullable=False)
    degree = db.Column(db.String(50), nullable=False)
    tuition_preference = db.Column(db.String(50), nullable=False)
    room_preference = db.Column(db.String(50), nullable=False)

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
@app.route("/", methods=['POST'])
def renderHome():
    form = SchoolForm()
    if form.validate_on_submit():
        return render_template('home.html', data="It worked!")
    return render_template('home.html')


# Route for search results 
@app.route("/search-results", methods=['GET'])
def renderHome():
    return render_template('searchResults.html')


# Route for chosen college
@app.route("/", methods=['GET'])
def renderHome():
    return render_template('college.html')


# Route for a database page (meant for testing purposes)
@app.route("/db")
def renderDb():
    all_school_data = Schools.query.all()
    return render_template('database.html', all_school_data=all_school_data)