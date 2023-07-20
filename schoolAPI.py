'''
Doesn't serve a purpose anymore, was created simply to demonstrate
functionality of the API along with how to parse specific data.
'''

# import requests

# url = 'http://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&school.name=Florida%20International%20University'
# API_KEY = 'ZYAlvWEGb09f4OJPE7lH5Z7Y7bQyzw0N72NogF6h'

# params = {
#     'api_key': API_KEY
# }

# response = requests.get(url, params=params).json()

# # Prints all the general school info
# print(response["results"][0]["latest"]["school"]["name"])

# # Prints all the cost info pertaining to that school
# print(response["results"][0]["latest"]["cost"])

# # Prints all the financial aid info pertaining to that school
# print(response["results"][0]["latest"]["aid"])

# Prints all the program titles with their corresponding degree types
# response = response["results"][0]["latest"]["programs"]["cip_4_digit"]

# i = 0
# while i < len(response):
#     print()
#     print(f"Program: {response[i]['title']}")
#     print(f"Degree: {response[i]['credential']['title']}")
#     i += 1