import requests

HOST = 'http://127.0.0.1:8080/'

#  USER
# response = requests.post(HOST + 'user',
#                          json={'name': 'Antonyio', 'password': '457375KUG'})
# print(response.status_code)
# print(response.json())

# user_id = response.json()['id']

# response = requests.get(HOST + f'user/{1}')
# print(response.status_code)
# print(response.text)

#   ADVERT
# response = requests.post(HOST + 'advert',
#                          json={'title': 'Garaj', 'body': 'Sale garaj', 'owner_id': 3})
# print(response.status_code)
# print(response.json())

# response = requests.get(HOST + f'advert/{5}')
# print(response.status_code)
# print(response.text)

response = requests.delete(HOST + f'advert/{5}')
print(response.status_code)
print(response.text)