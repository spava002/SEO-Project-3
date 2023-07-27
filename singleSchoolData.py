# FILENAME: singleSchoolData.py
# DATE: July 19th, 2023
# DESCRIPTION: This program is used to gather key infromation from a school using the College Scorecard API.
#              The information is meant to be used when clicking on a school name in our website's search
#              results to gather the necessary information about the school for posting.

import requests
import matplotlib.pyplot as plt

class School:
    def __init__(self, response):
        '''Initializes member variables that hold key information about the specified school'''
        # School Name
        self.name = response['results'][0]['latest']['school']['name']

        # Location Info
        self.city = response['results'][0]['latest']['school']['city']
        self.state = response['results'][0]['latest']['school']['state']

        # School Facts
        self.student_size = response['results'][0]['latest']['student']['size']
        if response['results'][0]['latest']['student']['grad_students'] is None:
            self.is_undergraduate_only = 'Yes'
        else:
            self.is_undergraduate_only = 'No'

        # Cost of Attendance Info
        self.tuition_in_state = response['results'][0]['latest']['cost']['tuition']['in_state']
        self.tuition_out_of_state = response['results'][0]['latest']['cost']['tuition']['out_of_state']
        self.roomboard_on_campus = response['results'][0]['latest']['cost']['roomboard']['oncampus']
        self.roomboard_off_campus = response['results'][0]['latest']['cost']['roomboard']['offcampus']
        self.booksupply = response['results'][0]['latest']['cost']['booksupply']

        # Financial Aid Info
        # self.percent_receiving_pell_grant = (not necessary?)
        # self.percent_receiving_federal_loan = (not necessary?)
        self.average_overall_net_price = response['results'][0]['latest']['cost']['avg_net_price']['overall']
        
        # Admissions Info
        self.acceptance_rate = response['results'][0]['latest']['admissions']['admission_rate']['overall']
        self.average_SAT_score = response['results'][0]['latest']['admissions']['sat_scores']['average']['overall']
        self.average_ACT_score = response['results'][0]['latest']['admissions']['act_scores']['midpoint']['cumulative']

        # Demographics
        self.percent_male = response['results'][0]['latest']['student']['demographics']['men']
        self.percent_female = response['results'][0]['latest']['student']['demographics']['women']
        self.percent_native_american = response['results'][0]['latest']['student']['demographics']['race_ethnicity']['aian']
        self.percent_native_hawaiian_pacific_islander = response['results'][0]['latest']['student']['demographics']['race_ethnicity']['nhpi']
        self.percent_asian =  response['results'][0]['latest']['student']['demographics']['race_ethnicity']['asian']
        self.percent_black = response['results'][0]['latest']['student']['demographics']['race_ethnicity']['black']
        self.percent_white = response['results'][0]['latest']['student']['demographics']['race_ethnicity']['white']
        self.percent_hispanic = response['results'][0]['latest']['student']['demographics']['race_ethnicity']['hispanic']
        self.percent_ethnicity_unknown = response['results'][0]['latest']['student']['demographics']['race_ethnicity']['unknown']

        # Top 5 Majors For Desired School
        self.most_popular_majors = fetch_most_popular_majors(response)

        # Links
        self.school_website_url = response['results'][0]['latest']['school']['school_url']
        self.price_calculator_website_url = response['results'][0]['latest']['school']['price_calculator_url']
        
    def plot_gender_demographics_pie_chart(self, schoolNum):
        # Data for the pie chart
        labels = ['Male', 'Female']
        sizes = [self.percent_male, self.percent_female]
        colors = ['dodgerblue', 'orange']
        explode = (0.1, 0)  # Explode any slices if needed

        # Plotting the pie chart
        plt.figure(figsize = (8, 8))  # Adjust the figure size if needed
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Plot Title
        plt.title(f'Gender Makeup at {self.name}')

        # Save the pie chart as a PNG file
        plt.savefig("static/images/gender_demographics_pie_chart" + str(schoolNum) + ".png")
    
    def plot_racial_demographics_pie_chart(self, schoolNum):
        # Data for the pie chart
        if (self.percent_native_american +  self.percent_native_hawaiian_pacific_islander + self.percent_ethnicity_unknown) < 0.05:
            labels = ['Other', 'Asian', 'Black', 'White', 'Hispanic']
            sizes = [self.percent_native_american + self.percent_native_hawaiian_pacific_islander + self.percent_ethnicity_unknown, self.percent_asian, self.percent_black, self.percent_white, self.percent_hispanic]
            colors = ['red', 'orange', 'yellow', 'green', 'dodgerblue']
            explode = (0, 0, 0, 0, 0)  # Explode any slices if needed
        elif self.percent_native_american + self.percent_native_hawaiian_pacific_islander < 0.05:
            labels = ['Native American,\nNative Hawaiian/\nPacific Islander', 'Asian', 'Black', 'White', 'Hispanic', 'Ethnicity Unknown']
            sizes = [self.percent_native_american + self.percent_native_hawaiian_pacific_islander, self.percent_asian, self.percent_black, self.percent_white, self.percent_hispanic, self.percent_ethnicity_unknown]
            colors = ['red', 'orange', 'yellow', 'green', 'dodgerblue', 'purple']
            explode = (0, 0, 0, 0, 0, 0)  # Explode any slices if needed
    
        # Plotting the pie chart
        plt.figure(figsize=(8, 8))  # Adjust the figure size if needed
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
        # Plot Title
        plt.title(f'Racial Demographics at {self.name}', y= 1.025)
        # plt.tight_layout()  # Ensures that the label is not cut off
    
        # Save the pie chart as a PNG file
        plt.savefig("static/images/racial_demographics_pie_chart" + str(schoolNum) + ".png")


def getResponse(url):
    '''This helper function accesses our API to return the JSON file with school information'''
    API_KEY = 'sHT6C7GtKya3ihqLt0Ji4NShHfwyIX8dGKbT6znD'
    params = {
        'api_key': API_KEY
    }
    response = requests.get(url, params=params).json()
    return response


def singleSearch(school_name, schoolNum=1):
    # Specify school...
    url = 'http://api.data.gov/ed/collegescorecard/v1/schools.json?school.name=' + school_name
    response = getResponse(url)
    if len(response['results']) == 0:
        return None
    mySchool = School(response)

    return generateSchoolData(mySchool, schoolNum)


def fetch_most_popular_majors(response):
    num_degree_types_ever_awarded = len(response["results"][0]["latest"]["programs"]["cip_4_digit"]) # The number of degree types ever awarded -- even if its not a current major/degree. (I think? My school has some degrees it doesn't give out)
    num_graduates_by_major = []
    for i in range(num_degree_types_ever_awarded):
        major_name = response["results"][0]["latest"]["programs"]["cip_4_digit"][i]["title"]
        num_graduates_with_this_major = response["results"][0]["latest"]["programs"]["cip_4_digit"][i]['counts']['ipeds_awards2']
        type_of_degree = response["results"][0]["latest"]["programs"]["cip_4_digit"][i]['credential']['title']
        num_graduates_by_major.append([major_name, type_of_degree, num_graduates_with_this_major])

    # Sorting function to handle None values inside of num_graduates_by_major
    def custom_sort(item):
        return item[2] if item[2] is not None else float('-inf')

    # Sort the data in descending order based on the number of people in each major
    sorted_data = sorted(num_graduates_by_major, key=custom_sort, reverse=True)

    # Get the top 5 most popular majors
    top_5_majors = sorted_data[:5]

    # Print the result
    return top_5_majors


def generateSchoolData(mySchool, schoolNum):
    '''This helper function prints out all variable values in our School object to help debug/view for correct output'''
    singleSchoolData = {}
    # print('-----> Location Info <-----')
    # print()

    # print(f'College City:                               {mySchool.city}')
    # print(f'College State:                              {mySchool.state}')

    locationInfo = [mySchool.city + " " + mySchool.state]
    singleSchoolData.update({"locationInfo": locationInfo})

    # print()
    # print('-----> School Facts <-----')
    # print()

    # print(f'Student Size:                               {mySchool.student_size}')
    # print(f'Undergraduate Only?:                        {mySchool.is_undergraduate_only}')

    schoolFacts = [mySchool.student_size, mySchool.is_undergraduate_only]
    if schoolFacts[0] == None:
        schoolFacts[0] = 0
    singleSchoolData.update({"schoolFacts": schoolFacts})

    # print()
    # print('-----> Cost of Attendance Info <-----')
    # print()

    # print(f'In-State Tuition:                           {mySchool.tuition_in_state}')
    # print(f'Out-of-State Tuition:                       {mySchool.tuition_out_of_state}')
    # print(f'Roomboard On-Campus Cost:                   {mySchool.roomboard_on_campus}')
    # print(f'Roomboard Off-Campus Cost:                  {mySchool.roomboard_off_campus}')
    # print(f'Booksupply Cost:                            {mySchool.booksupply}')

    costOfAttendanceInfo = [mySchool.tuition_in_state, mySchool.tuition_out_of_state, mySchool.roomboard_on_campus, mySchool.roomboard_off_campus, mySchool.booksupply]
    for i in range(len(costOfAttendanceInfo)):
        if costOfAttendanceInfo[i] == None:
            costOfAttendanceInfo[i] = 0
    singleSchoolData.update({"costOfAttendanceInfo": costOfAttendanceInfo})

    # print()
    # print('-----> Financial Aid Info <-----')
    # print()

    # print(f'Average Net Cost (after aid):               {mySchool.average_overall_net_price}')

    financialAidInfo = [mySchool.average_overall_net_price]
    if financialAidInfo[0] == None:
        financialAidInfo[0] = 0
    singleSchoolData.update({"financialAidInfo": financialAidInfo})
   
    # print()
    # print('-----> Admissions Info <-----')
    # print()
    # print(f'Acceptance Rate:                            {mySchool.acceptance_rate}')
    # print(f'Average SAT Score:                          {mySchool.average_SAT_score}')
    # print(f'Average ACT Score:                          {mySchool.average_ACT_score}')

    admissionsInfo = [mySchool.acceptance_rate, mySchool.average_SAT_score, mySchool.average_ACT_score]
    for i in range(len(admissionsInfo)):
        if admissionsInfo[i] == None:
            admissionsInfo[i] = 0
    singleSchoolData.update({"admissionsInfo": admissionsInfo})
    
    # print()
    # print('-----> Demographics <-----')
    # print()
    
    # print(f'Percent Male:                               {mySchool.percent_male}')
    # print(f'Percent Female:                             {mySchool.percent_female}')
    # print(f'Percent Native American:                    {mySchool.percent_native_american}')
    # print(f'Percent Native Hawaiian/Pacific Islander:   {mySchool.percent_native_hawaiian_pacific_islander}')
    # print(f'Percent Asian:                              {mySchool.percent_asian}')
    # print(f'Percent Black:                              {mySchool.percent_black}')
    # print(f'Percent White:                              {mySchool.percent_white}')
    # print(f'Percent Hispanic:                           {mySchool.percent_hispanic}')
    # print(f'Percent Ethnicity Unknown:                  {mySchool.percent_ethnicity_unknown}')

    demographicsInfo = [mySchool.percent_male, mySchool.percent_female, mySchool.percent_native_american, mySchool.percent_native_hawaiian_pacific_islander, mySchool.percent_asian, mySchool.percent_black, mySchool.percent_white, mySchool.percent_hispanic, mySchool.percent_ethnicity_unknown]
    for i in range(len(demographicsInfo)):
        if demographicsInfo[i] == None:
            demographicsInfo[i] = 0
    singleSchoolData.update({"demographicsInfo": demographicsInfo})
    
    # print()
    # print('-----> Degrees Offered <-----')
    # print()

    # print(f'Programs and Corresponding Degrees Offered:\n {mySchool.program_to_degree}') # NOTE: Returns a dictionary!

    # Replacement code for programs/degrees until more compressed solution is offered
    topMajors = mySchool.most_popular_majors
    singleSchoolData.update({"topMajors":topMajors})
    
    # print()
    # print('-----> External Links <-----')
    # print()
  
    # print(f'School Website URL:                         {mySchool.school_website_url}')
    # print(f'Price Calculator Website:                   {mySchool.price_calculator_website_url}')
    # print()

    externalLinks = [mySchool.school_website_url, mySchool.price_calculator_website_url]
    singleSchoolData.update({"externalLinks": externalLinks})
    mySchool.plot_gender_demographics_pie_chart(schoolNum)
    mySchool.plot_racial_demographics_pie_chart(schoolNum)

    return singleSchoolData
