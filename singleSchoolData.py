# FILENAME: singleSchoolData.py
# DATE: July 19th, 2023
# DESCRIPTION: This program is used to gather key infromation from a school using the College Scorecard API.
#              The information is meant to be used when clicking on a school name in our website's search
#              results to gather the necessary information about the school for posting.

import requests

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

        # Degrees Offered
        self.areas_of_study = []
        self.degree_type = []
        for program in response['results'][0]['latest']['programs']['cip_4_digit']:
            self.areas_of_study.append(program['title'])
            self.degree_type.append(program['credential']['title'])
    
        # Make dictionary where self.areas_of_study[i] : self.degree_type[i] --> aka, dictonary has the format --> Program Name (like Chemistry) : Degree Type (bachlor's, masters, etc.)
        self.program_to_degree = {}
        for i in range(len(self.areas_of_study)):
            programTitle = self.areas_of_study[i]
            degreeType = self.degree_type[i]
            self.program_to_degree[programTitle] = degreeType

        # Links
        self.school_website_url = response['results'][0]['latest']['school']['school_url']
        self.price_calculator_website_url = response['results'][0]['latest']['school']['price_calculator_url']

def getResponse(url):
    '''This helper function accesses our API to return the JSON file with school information'''
    API_KEY = 'sHT6C7GtKya3ihqLt0Ji4NShHfwyIX8dGKbT6znD'
    params = {
        'api_key': API_KEY
    }
    response = requests.get(url, params=params).json()
    return response

def main(degree, residency, school_type, tuition_preference, room_preference):
    # Prints out the received form data
    print(f"Chosen Degree is {degree}") 
    print(f"Chosen Reisidency is {residency}") 
    print(f"Chosen School Type is {school_type}") 
    print(f"Chosen Tuition Preference is $0-${tuition_preference}") 
    print(f"Chosen Room Preference is $0-${room_preference}") 

    # Specify school...
    schoolName = 'Harvard'
    url = 'http://api.data.gov/ed/collegescorecard/v1/schools.json?school.name=' + schoolName
    response = getResponse(url)
    mySchool = School(response)

    # This function call below can be deleted, it was to debug/view variable outputs.
    optional_view_variables(mySchool)

def optional_view_variables(mySchool):
    '''This helper function prints out all variable values in our School object to help debug/view for correct output'''
    print('-----> Location Info <-----')
    print()

    print(f'College City:                               {mySchool.city}')
    print(f'College State:                              {mySchool.state}')

    print()
    print('-----> School Facts <-----')
    print()

    print(f'Student Size:                               {mySchool.student_size}')
    print(f'Undergraduate Only?:                        {mySchool.is_undergraduate_only}')

    print()
    print('-----> Cost of Attendance Info <-----')
    print()

    print(f'In-State Tuition:                           {mySchool.tuition_in_state}')
    print(f'Out-of-State Tuition:                       {mySchool.tuition_out_of_state}')
    print(f'Roomboard On-Campus Cost:                   {mySchool.roomboard_on_campus}')
    print(f'Roomboard Off-Campus Cost:                  {mySchool.roomboard_off_campus}')
    print(f'Booksupply Cost:                            {mySchool.booksupply}')
    print()
    print('-----> Financial Aid Info <-----')
    print()

    print(f'Average Net Cost (after aid):               {mySchool.average_overall_net_price}')
   
    print()
    print('-----> Admissions Info <-----')
    print()
    print(f'Acceptance Rate:                            {mySchool.acceptance_rate}')
    print(f'Average SAT Score:                          {mySchool.average_SAT_score}')
    print(f'Average ACT Score:                          {mySchool.average_ACT_score}')
    
    print()
    print('-----> Demographics <-----')
    print()
    
    print(f'Percent Male:                               {mySchool.percent_male}')
    print(f'Percent Female:                             {mySchool.percent_female}')
    print(f'Percent Native American:                    {mySchool.percent_native_american}')
    print(f'Percent Native Hawaiian/Pacific Islander:   {mySchool.percent_native_hawaiian_pacific_islander}')
    print(f'Percent Asian:                              {mySchool.percent_asian}')
    print(f'Percent Black:                              {mySchool.percent_black}')
    print(f'Percent White:                              {mySchool.percent_white}')
    print(f'Percent Hispanic:                           {mySchool.percent_hispanic}')
    print(f'Percent Ethnicity Unknown:                  {mySchool.percent_ethnicity_unknown}')
    
    print()
    print('-----> Degrees Offered <-----')
    print()

    print(f'Programs and Corresponding Degrees Offered:\n {mySchool.program_to_degree}') # NOTE: Returns a dictionary!
    
    print()
    print('-----> External Links <-----')
    print()
  
    print(f'School Website URL:                         {mySchool.school_website_url}')
    print(f'Price Calculator Website:                   {mySchool.price_calculator_website_url}')
    print()

# Run Program
# main()
