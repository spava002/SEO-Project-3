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
    # id, degree, and residency will always contain a value
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(50), nullable=False)
    residency = db.Column(db.String(50), nullable=False)
    # school_type, tuition_preference, and room_preference won't always contain a value
    school_type = db.Column(db.String(50), nullable=False)
    tuition_preference = db.Column(db.Integer(50), nullable=False)
    room_preference = db.Column(db.Integer(50), nullable=False)

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
    form = SchoolForm()
    if form.validate_on_submit():
        return redirect(url_for('renderSearchResults', data="It worked!"))
    return render_template('home.html', filteredForm=form)


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