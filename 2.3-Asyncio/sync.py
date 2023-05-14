import requests

def get_people(people_id):

    return requests.get(f'https://swapi.dev/api/people/{people_id}').json()


def main():
    response = get_people(1)
    print(response)
    response = get_people(2)
    print(response)



main()