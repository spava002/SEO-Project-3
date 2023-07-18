import requests

url = 'http://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&school.name=Florida%20International%20University'
API_KEY = 'ZYAlvWEGb09f4OJPE7lH5Z7Y7bQyzw0N72NogF6h'

params = {
    'api_key': API_KEY
}

response = requests.get(url, params=params).json()

# Prints all the general school info
print(response["results"][0]["school"])

# Prints all the cost info pertaining to that school
print(response["results"][0]["latest"]["cost"])

# Prints all the financial aid info pertaining to that school
print(response["results"][0]["latest"]["aid"])