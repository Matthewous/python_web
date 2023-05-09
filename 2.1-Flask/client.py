import requests


response = requests.delete('http://127.0.0.1:5001/adv/2')
print(response.status_code)
print(response.json())


response = requests.patch('http://127.0.0.1:5001/adv/3', json={'title': 'title', 'description': 'descr', 'owner': 'me' })
print(response.status_code)
print(response.json())


response = requests.get('http://127.0.0.1:5001/adv/2')
print(response.status_code)
print(response.json())


response = requests.post('http://127.0.0.1:5001/adv', json={'title': 'new_title', 'description': 'new_descr', 'owner': 'me_too' })
print(response.status_code)
print(response.json())