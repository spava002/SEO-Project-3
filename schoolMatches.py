# FILE: schoolMatches.py
# DATE: July 20th, 2023
# DESCRIPTION: This program is meant to take in user specified filters for a college 
#              and return the colleges that meet their specifications.

import requests
import json

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

def extract_upper_price(price_range_string):
    '''Function to extract the upper price range of tuition_preference and room_preference'''
    # Split the price string based on the "-" character
    parts = price_range_string.split('-')
    # Extract the upper price range (second part of the split)
    upper_price = parts[1]
    # Remove any whitespace and the dollar sign ('$') from the upper price range
    upper_price = upper_price.strip().replace('$', '')
    
    return upper_price

def main(degree, residency, residency_preference, school_type_preference, tuition_preference, room_preference):
    degree_name = f'&programs.cip_4_digit.title={degree}.'
    tuition_upper_price = extract_upper_price(tuition_preference)
    # room_upper_price = extract_upper_price(room_preference) FIXME: not used since can't filter by housing prices.

    # If out-of-state, find schools and costs for out-of-state
    if residency_preference == 'outofstate':
        school_state = f'&school.state__not={us_states_and_territories[residency]}'
        tuition_price_range = f'&latest.cost.tuition.out_of_state__range=0..{tuition_upper_price}'

    # Elif preference is in-state, find schools and costs for in-state
    elif residency_preference == 'instate':
        school_state = f'&school.state={us_states_and_territories[residency]}'
        tuition_price_range = f'&latest.cost.tuition.in_state__range=0..{tuition_upper_price}'

    # Else, return schools in all states. TODO: calculate costs accordingly (ie. depending on homestate, give in-state or out-of-state pricing)
    else:
        school_state = '' # no preference for states
        # Default to show out-of-state pricing for now!
        tuition_price_range = f'&latest.cost.tuition.out_of_state__range=0..{tuition_upper_price}'
       
    # Logic for displaying either private or public schools depending on preference
    if school_type_preference == 'private':
        school_type = '&school.ownership=2,3'
    elif school_type_preference == 'public':
        school_type = '&school.ownership=1'
    else:
        school_type = '' # no preference for school type, show both public and private schools

    # Defaulting to on-campus pricing for housing range (FIXME: NOT ABLE TO FILTER WITH THIS PARAM!!!
    # room_price_range =  f'&latest.cost.roomboard.oncampus__range=0..{room_upper_price}'

    # Possible Filter categories... If one sounds interesting, let me know and I'll get you more in-depth decriptions about each one!
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

    # Categories above are possible future additions since filtering by room price wasn't a filter option with our API.


    url = f'http://api.data.gov/ed/collegescorecard/v1/schools.json?_fields=school.name{degree_name}{school_state}{tuition_price_range}{school_type}&per_page=100'

    response = get_api_response(url)
    school_matches = [school["school.name"] for school in response["results"]]   
    print()
    print(school_matches) 
    print()
    print(f'This query returned {len(school_matches)} matches!')
    print()
    return school_matches



# Note: final param, room_tuition_preference can't be used as a filter in our API.
main('Computer Engineering', 'california', 'outofstate', 'private', '$0-$40000', 'cant be used')

# This function call returns 94 school results. How should I pick the "top" 5 schools to show on the results page? or should i just return all of them? Right now all are returned.
# I was thinking maybe showing top 5 by college ranking? this would require another API though since ours doesn't include this information.

# Also keep in mind that this API limits results on a page to 100 schools. So if more than 100 schools are a result, we have to make another API call but specifying '&page=2'
# which would slow processing time?


    
