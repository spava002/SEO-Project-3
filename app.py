from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from filteredForm import SchoolForm
from unfilteredForm import SchoolNameForm
from signUpForm import signUp
from loginForm import login
from singleSchoolData import singleSearch
from schoolMatches import multipleSearch
import git
import logging


app = Flask(__name__)
app.config['SECRET_KEY'] = 'PS7T6txPuOaXKkNnvToX90e0J'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schools.db'

db = SQLAlchemy(app)


class Schools(db.Model):
    # id, degree, and residency will always contain a value
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    multiple_search = db.Column(db.Boolean, nullable=False)
    school_name = db.Column(db.String(50), nullable=False)
    location_info = db.Column(db.String(50), nullable=False)
    student_size = db.Column(db.Integer, nullable=False)
    is_undergraduate_only = db.Column(db.String(50), nullable=False)
    in_state_tuition = db.Column(db.Integer, nullable=False)
    out_state_tuition = db.Column(db.Integer, nullable=False)
    roomboard_on_campus = db.Column(db.Integer, nullable=False)
    roomboard_off_campus = db.Column(db.Integer, nullable=False)
    book_supply = db.Column(db.Integer, nullable=False)
    average_overall_net_price = db.Column(db.Integer, nullable=False)
    acceptance_rate = db.Column(db.Float, nullable=False)
    avg_SAT_score = db.Column(db.Integer, nullable=False)
    avg_ACT_score = db.Column(db.Integer, nullable=False)
    percent_male = db.Column(db.Float, nullable=False)
    percent_female = db.Column(db.Float, nullable=False)
    percent_native_american = db.Column(db.Float, nullable=False)
    percent_native_hawaiian_pacific_islander = db.Column(db.Float, nullable=False)
    percent_asian = db.Column(db.Float, nullable=False)
    percent_black = db.Column(db.Float, nullable=False)
    percent_white = db.Column(db.Float, nullable=False)
    percent_hispanic = db.Column(db.Float, nullable=False)
    percent_ethnicity_unknown = db.Column(db.Float, nullable=False)
    first_degree_offered = db.Column(db.String(100), nullable=False)
    second_degree_offered = db.Column(db.String(100), nullable=False)
    third_degree_offered = db.Column(db.String(100), nullable=False)
    fourth_degree_offered = db.Column(db.String(100), nullable=False)
    fifth_degree_offered = db.Column(db.String(100), nullable=False)
    school_website_url = db.Column(db.String(100), nullable=False)
    price_calculator_website = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return ""


with app.app_context():
    db.create_all()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

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


@app.route("/", methods=['POST', 'GET'])
def userLogin():
    loginForm = login()
    if loginForm.validate_on_submit():
        username = loginForm.username.data
        password = loginForm.password.data
        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            logging.info("User has successfully logged in!")
            session['user'] = username
            return redirect(url_for("renderHome"))
        else:
            flash("Invalid username or password!", "error")
    return render_template("login.html", loginForm=loginForm, signUpForm=signUp())



@app.route("/signup", methods=['POST', 'GET'])
def userSignUp():
    signUpForm = signUp()
    if signUpForm.validate_on_submit():
        username = signUpForm.username.data
        password = signUpForm.password.data
        user = Users.query.filter_by(username=username).first()
        if user:
            print("User is already taken!")
            flash("User is already taken, try again.", "error")
        else:
            user_data = Users(username=username, password=password)
            db.session.add(user_data)
            db.session.commit()
            logging.info(f"User data was added successfully!")
            session['user'] = username
            return redirect(url_for("renderHome"))
    return render_template("login.html", loginForm=login(), signUpForm=signUpForm)


# Route for home page
@app.route("/home", methods=['POST', 'GET'])
def renderHome():
    user = session.get('user')
    filteredForm = SchoolForm()
    unfilteredForm = SchoolNameForm()
    if filteredForm.validate_on_submit():
        degree = filteredForm.degree.data
        residency = filteredForm.residency.data
        residency_preference = filteredForm.residency_preference.data
        school_type = filteredForm.school_type.data
        tuition_preference = filteredForm.tuition_preference.data
        # average_cost_of_attendance = filteredForm.average_cost_of_attendance.data
        school_matches = multipleSearch(degree, residency, residency_preference, school_type, tuition_preference)
        firstFiveSchools = []
        upper_search_limit = 5
        if len(school_matches) < 5:
            upper_search_limit = len(school_matches)
        for i in range(0, upper_search_limit):
            singleSchoolData = singleSearch(school_matches[i])
            single_school_data = Schools(user=user, multiple_search=True, school_name=school_matches[i], location_info=singleSchoolData["locationInfo"][0], student_size=singleSchoolData["schoolFacts"][0], is_undergraduate_only=singleSchoolData["schoolFacts"][1], in_state_tuition=singleSchoolData["costOfAttendanceInfo"][0], out_state_tuition=singleSchoolData["costOfAttendanceInfo"][1], roomboard_on_campus=singleSchoolData["costOfAttendanceInfo"][2], roomboard_off_campus=singleSchoolData["costOfAttendanceInfo"][3], book_supply=singleSchoolData["costOfAttendanceInfo"][4], average_overall_net_price=singleSchoolData["financialAidInfo"][0], acceptance_rate=singleSchoolData["admissionsInfo"][0], avg_SAT_score=singleSchoolData["admissionsInfo"][1], avg_ACT_score=singleSchoolData["admissionsInfo"][2], percent_male=singleSchoolData["demographicsInfo"][0], percent_female=singleSchoolData["demographicsInfo"][1], percent_native_american=singleSchoolData["demographicsInfo"][2], percent_native_hawaiian_pacific_islander=singleSchoolData["demographicsInfo"][3], percent_asian=singleSchoolData["demographicsInfo"][4], percent_black=singleSchoolData["demographicsInfo"][5], percent_white=singleSchoolData["demographicsInfo"][6], percent_hispanic=singleSchoolData["demographicsInfo"][7], percent_ethnicity_unknown=singleSchoolData["demographicsInfo"][8], first_degree_offered=singleSchoolData["topMajors"][0][1] + " in " + singleSchoolData["topMajors"][0][0] + " with currently " + str(singleSchoolData["topMajors"][0][2]) + " students.", second_degree_offered=singleSchoolData["topMajors"][1][1] + " in " + singleSchoolData["topMajors"][1][0] + " with currently " + str(singleSchoolData["topMajors"][1][2]) + " students.", third_degree_offered=singleSchoolData["topMajors"][2][1] + " in " + singleSchoolData["topMajors"][2][0] + " with currently " + str(singleSchoolData["topMajors"][2][2]) + " students.", fourth_degree_offered=singleSchoolData["topMajors"][3][1] + " in " + singleSchoolData["topMajors"][3][0] + " with currently " + str(singleSchoolData["topMajors"][3][2]) + " students.", fifth_degree_offered=singleSchoolData["topMajors"][4][1] + " in " + singleSchoolData["topMajors"][4][0] + " with currently " + str(singleSchoolData["topMajors"][4][2]) + " students.", school_website_url=singleSchoolData["externalLinks"][0], price_calculator_website=singleSchoolData["externalLinks"][1])
            db.session.add(single_school_data)
            db.session.commit()
            logging.info(f"School data was added successfully!")
            firstFiveSchools.append(single_school_data)
        return render_template('searchResults.html', firstFiveSchools=firstFiveSchools)
    elif unfilteredForm.validate_on_submit():
        school_name = unfilteredForm.school_name.data
        singleSchoolData = singleSearch(school_name)
        single_school_data = Schools(user=user, multiple_search=False, school_name=school_name, location_info=singleSchoolData["locationInfo"][0], student_size=singleSchoolData["schoolFacts"][0], is_undergraduate_only=singleSchoolData["schoolFacts"][1], in_state_tuition=singleSchoolData["costOfAttendanceInfo"][0], out_state_tuition=singleSchoolData["costOfAttendanceInfo"][1], roomboard_on_campus=singleSchoolData["costOfAttendanceInfo"][2], roomboard_off_campus=singleSchoolData["costOfAttendanceInfo"][3], book_supply=singleSchoolData["costOfAttendanceInfo"][4], average_overall_net_price=singleSchoolData["financialAidInfo"][0], acceptance_rate=singleSchoolData["admissionsInfo"][0], avg_SAT_score=singleSchoolData["admissionsInfo"][1], avg_ACT_score=singleSchoolData["admissionsInfo"][2], percent_male=singleSchoolData["demographicsInfo"][0], percent_female=singleSchoolData["demographicsInfo"][1], percent_native_american=singleSchoolData["demographicsInfo"][2], percent_native_hawaiian_pacific_islander=singleSchoolData["demographicsInfo"][3], percent_asian=singleSchoolData["demographicsInfo"][4], percent_black=singleSchoolData["demographicsInfo"][5], percent_white=singleSchoolData["demographicsInfo"][6], percent_hispanic=singleSchoolData["demographicsInfo"][7], percent_ethnicity_unknown=singleSchoolData["demographicsInfo"][8], first_degree_offered=singleSchoolData["topMajors"][0][1] + " in " + singleSchoolData["topMajors"][0][0] + " with currently " + str(singleSchoolData["topMajors"][0][2]) + " students.", second_degree_offered=singleSchoolData["topMajors"][1][1] + " in " + singleSchoolData["topMajors"][1][0] + " with currently " + str(singleSchoolData["topMajors"][1][2]) + " students.", third_degree_offered=singleSchoolData["topMajors"][2][1] + " in " + singleSchoolData["topMajors"][2][0] + " with currently " + str(singleSchoolData["topMajors"][2][2]) + " students.", fourth_degree_offered=singleSchoolData["topMajors"][3][1] + " in " + singleSchoolData["topMajors"][3][0] + " with currently " + str(singleSchoolData["topMajors"][3][2]) + " students.", fifth_degree_offered=singleSchoolData["topMajors"][4][1] + " in " + singleSchoolData["topMajors"][4][0] + " with currently " + str(singleSchoolData["topMajors"][4][2]) + " students.", school_website_url=singleSchoolData["externalLinks"][0], price_calculator_website=singleSchoolData["externalLinks"][1])
        db.session.add(single_school_data)
        db.session.commit()
        logging.info(f"School data was added successfully!")
        return render_template("searchResults.html", single_school_data=single_school_data)
        # return redirect(url_for('renderSearchResults', data="The unfiltered form was submitted!", single_school_data=single_school_data))
    
    return render_template('home.html', user=user, filteredForm=filteredForm, unfilteredForm=unfilteredForm)


# Route for search results 
@app.route("/search-results", methods=['GET'])
def renderSearchResults():
    data = request.args.get('data')
    return render_template('searchResults.html', data=data)


# Route for a user history page (meant for testing purposes)
@app.route("/history")
def renderSearchHistory():
    user = session.get('user')
    user_search_history = Schools.query.filter(Schools.user == user).all()
    return render_template("history.html", user=user, user_search_history=user_search_history)


# Route that allows deleting of user history
@app.route('/delete-history/<int:id>')
def delete_history(id):
    school = Schools.query.get_or_404(id)

    try:
        db.session.delete(school)
        db.session.commit()
        return redirect(url_for('renderSearchHistory'))
    except Exception as e:
        logging.error(f"There was an error deleting that: {e}")
        return "There was an error deleting that!"


# Route for a database page (meant for testing purposes)
@app.route("/db")
def renderDb():
    all_school_data = Schools.query.all()
    return render_template('db.html', all_school_data=all_school_data)


# Route that allows deleting of database data (Meant for experimental use)
@app.route('/delete-school/<int:id>')
def delete_school(id):
    school = Schools.query.get_or_404(id)

    try:
        db.session.delete(school)
        db.session.commit()
        return redirect(url_for('renderDb'))
    except Exception as e:
        logging.error(f"There was an error deleting that: {e}")
        return "There was an error deleting that!"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")