# FILE: schoolMatches.py
# DATE: July 20th, 2023
# DESCRIPTION: This program is meant to take in user specified filters for a college 
#              and return the colleges that meet their specifications.

import requests
from title_code_dict import title_code_dict # To access "major name: major code number" dictionary

us_states_and_territories = {
    "alabama": "AL",
    "alaska": "AK",
    "arizona": "AZ",
    "arkansas": "AR",
    "california": "CA",
    "colorado": "CO",
    "connecticut": "CT",
    "delaware": "DE",
    "florida": "FL",
    "georgia": "GA",
    "hawaii": "HI",
    "idaho": "ID",
    "illinois": "IL",
    "indiana": "IN",
    "iowa": "IA",
    "kansas": "KS",
    "kentucky": "KY",
    "louisiana": "LA",
    "maine": "ME",
    "maryland": "MD",
    "massachusetts": "MA",
    "michigan": "MI",
    "minnesota": "MN",
    "mississippi": "MS",
    "missouri": "MO",
    "montana": "MT",
    "nebraska": "NE",
    "nevada": "NV",
    "new hampshire": "NH",
    "new jersey": "NJ",
    "new mexico": "NM",
    "new york": "NY",
    "north carolina": "NC",
    "north dakota": "ND",
    "ohio": "OH",
    "oklahoma": "OK",
    "oregon": "OR",
    "pennsylvania": "PA",
    "rhode island": "RI",
    "south carolina": "SC",
    "south dakota": "SD",
    "tennessee": "TN",
    "texas": "TX",
    "utah": "UT",
    "vermont": "VT",
    "virginia": "VA",
    "washington": "WA",
    "west virginia": "WV",
    "wisconsin": "WI",
    "wyoming": "WY",
    "american samoa": "AS",
    "district of columbia": "DC",
    "guam": "GU",
    "northern mariana islands": "MP",
    "puerto rico": "PR",
    "u.s. virgin islands": "VI"
}

def get_api_response(url):
    '''This helper function accesses our API to return a JSON file with school information'''
    API_KEY = 'sHT6C7GtKya3ihqLt0Ji4NShHfwyIX8dGKbT6znD'
    params = {
        'api_key': API_KEY
    }
    response = requests.get(url, params=params).json()
    return response


def multipleSearch(degree, degree_type, residency, residency_preference, school_type_preference, tuition_preference): # NOTE! ADDED A NEW PARAM -- "DEGREE TYPE". SEARCH FOR SCHOOLS WITH TOP MATCHES BY DEGREE TYPE (EX. Bachelor's Degree, Master's Degree, etc.)
    '''This function takes in user filters and returns the top 5 college matches (sorted by the specified
       degree's popularity given most recent graduating class size) that meet all the filter criteria'''
    
    # If there is a degree type preference...
    if degree_type:
        degree_level = f'&programs.cip_4_digit.credential.title={degree_type}'

    # No degree type preference...
    else:
        degree_level = ''
    
    # Get majors in API that include user's keywords for the degree
    matching_majors_in_API = find_major_code(degree)
   
    # Extract number codes from the list of tuples using a list comprehension
    number_codes = [code for _, code in matching_majors_in_API]

    # Join the number codes into a single string using the join() method
    number_codes_string = ','.join(number_codes)

    # Assign the degree code(s) into an API sendable format
    degree_codes = f'&programs.cip_4_digit.code={number_codes_string}'

    # If out-of-state, find schools and costs for out-of-state
    if residency_preference == 'outofstate':
        school_state = f'&school.state__not={us_states_and_territories[residency]}'
        tuition_price_range = f'&latest.cost.tuition.out_of_state__range=0..{tuition_preference}'

    # Elif preference is in-state, find schools and costs for in-state
    elif residency_preference == 'instate':
        school_state = f'&school.state={us_states_and_territories[residency]}'
        tuition_price_range = f'&latest.cost.tuition.in_state__range=0..{tuition_preference}'

    # Else, return schools in all states. TODO: calculate costs accordingly (ie. depending on homestate, give in-state or out-of-state pricing)
    else:
        school_state = '' # no preference for states
        # Default to show out-of-state pricing for now!
        tuition_price_range = f'&latest.cost.tuition.out_of_state__range=0..{tuition_preference}'
       
    # Logic for displaying either private or public schools depending on preference
    if school_type_preference == 'private':
        school_type = '&school.ownership=2,3'
    elif school_type_preference == 'public':
        school_type = '&school.ownership=1'
    else:
        school_type = '' # no preference for school type, show both public and private schools

    url = f'http://api.data.gov/ed/collegescorecard/v1/schools.json?_fields=school.name,latest.programs.cip_4_digit{degree_codes}{degree_level}{school_state}{tuition_price_range}{school_type}&per_page=100'
    response = get_api_response(url)

    top_matches = []
    start = 0
    total_items = response['metadata']['total']
    items_per_page = response['metadata']['per_page']
    i = 0

    if degree_codes:
        # Loop API calls to gather information from each page if there are more than 100 results (API limits results to 100 per page, so make API calls incrementing page to get results from each page)
        while (start < total_items):
            url = f'http://api.data.gov/ed/collegescorecard/v1/schools.json?_fields=school.name,latest.programs.cip_4_digit{degree_codes}{school_state}{tuition_price_range}{school_type}&page={i}&per_page=100'
            response = get_api_response(url)
            # Every API Call, grab the top 5 schools from each page and extend them to the top_matches list
            top_matches.extend(fetch_most_popular_colleges_by_major(response, f'{degree}.'))
            start += items_per_page
            i += 1
        # Once each page has been iterated through, consolidate top_matches into just the top 5 overall schools with most recent graduates in the specified degree
        result = get_top_colleges_by_major_popularity(top_matches, degree_type, 5)

    # If result list isn't empty, return it
    if result:
        return result
    
    # If result list is empty, it means there were no matching schools.
    else:
        return None


def find_major_code(degree):
    '''Helper function to find matching majors and their codes in API generated dictionary "title_code_dict" based on user's input'''
    # Split the user's input into individual words
    keywords = degree.lower().replace(',', '').split()

    # List to store matching majors
    matching_majors = []

    # Loop through the keys in the dictionary
    for major, code in title_code_dict.items():
        # Convert the major name to lowercase for case-insensitive matching
        lower_major = major.lower()

        # Check if all keywords are present in the lowercased major name
        if all(keyword in lower_major for keyword in keywords):
            matching_majors.append((major, code))
            # print("Matching Major:", major)
            # print("Keywords:", keywords)
        # print(matching_majors)

    return matching_majors

    
def get_top_colleges_by_major_popularity(top_matches, degree_type, top_n):
    '''This helper function returns the top_n schools for a specified major and a specific major type. Note, a degree type 
       doesn't have to be specified, in which case schools with the most graduates for the user's specific major will be 
       shown, regardless of bachelor's, master's, etc.'''
    
    def custom_sort(item):
        '''Helper to define a custom sorting order based on the number of gradauates in the major'''
        return item[3] if item[3] is not None else float('-inf')
    
    # If degree_type preference...
    if not(degree_type == "None"):
        # Filter data based on the specified degree type
        filtered_data = [entry for entry in top_matches if entry[2] == degree_type]

        # Sort the filtered data in descending order based on the number of students
        sorted_data = sorted(filtered_data, key=custom_sort, reverse=True)

    # Else, no degree_type preference, default to show all degree_types in output
    else: 
        # Sort the data in descending order based on the number of people in each major
        sorted_data = sorted(top_matches, key=custom_sort, reverse=True)

    # Get the top_n colleges with the most students for the specified degree type
    top_colleges = sorted_data[:top_n]
    return top_colleges


def fetch_most_popular_colleges_by_major(response, target_major): # TODO: Maybe add another param to specify exact searches or exact + similar in terms of target_major being at a college?
    '''This function returns the top 5 schools with the most students in the specified major or similar major(similar major example: Biology, General and Molecular Biology)'''
    colleges_by_major = []

    # Iterate through each college
    for college_data in response['results']:

        # Iterate through each major at the current college
        for major_data in college_data['latest.programs.cip_4_digit']:
            major_name = major_data['title']
            degree_type = major_data['credential']['title']
            college_name = major_data['school']['name']
            num_graduates_with_this_major = major_data['counts']['ipeds_awards2']
            if num_graduates_with_this_major is not None:
                # Store the college and major name with number of graduates in a dictionary
                colleges_by_major.append([college_name, major_name, degree_type, num_graduates_with_this_major])
    return colleges_by_major


# TESTING
# These all print the same results! (Degree name doesn't matter if words are split by commas or spaces, it seperates degree input into keywords, 
# so for example, "Computer Science" becomes keywords = ["Computer","Science"] or "Mathematics, Computer Science" becomes keywords = ["Mathematics","Computer","Science"])
# It capitalization and order doesn't matter either! View below for examples that all return the same schools:
# print(multipleSearch("general engineering", "Bachelor's Degree", 'california', '', 'private', '70000'))
# print()
# print(multipleSearch("Engineering, General", "Bachelor's Degree", 'california', '', 'private', '70000'))
# print()
# print(multipleSearch("Engineering General", "Bachelor's Degree", 'california', '', 'private', '70000'))
# print()
# print(multipleSearch("GenErAl        EngiNeEring", "Bachelor's Degree", 'california', '', 'private', '70000'))




# EXTRA POSSIBLE FILTERS FOR FUTURE ADDITIONS...

# Possible Filter categories...
# 1) Test score requirements for admission
# 2) Overall median of completion rate
# 3) Overall median for average net price 
# 4) Overall median earnings of students working and not enrolled 10 years after entry
# 5) Average net price for $30,001-$48,000 family income (public institutions)               ---> Available for lots of income levels
# 6) Average SAT equivalent score of students admitted
# 7) Midpoint of the ACT cumulative score
# 8) Admission rate
# 9) Religous affiliation of the institution
# 10) Flag for women-only college
# 11) Flag for men-only college
# 12) Flag for Historically Black College and University
# 13) Flag for Hispanic-serving institution
# 14) Carnegie Classification -- size and setting                                            ---> examples are like 'Four-year, medium, highly residential') etc.
# 15) Carnegie Classification -- basic                                                       ---> examples are 'Master's Colleges & Universities: Larger Programs' or 'Special Focus Four-Year: Medical Schools & Centers') etc.
# 16) Degree of urbanization of institution                                                  ---> example is 'Mid-Size City (a central city of a CMSA or MSA, with the city having a population less than 250,000)' etc.
# 17) Locale of institution
# 18) Region (IPEDS)                                                                         ---> example: 'Rocky Mountains (CO, ID, MT, UT, WY)' or 'New England (CT, ME, MA, NH, RI, VT)', etc.
# 19) Highest degree awarded                                                                 ---> example: 'Non-degree-granting', 'Associate degree', 'Bachelor's degree', etc.