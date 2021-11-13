import requests

r = requests.get('http://localhost:3000/equivalents'
                 , json={'name': 'Amlozek 5 mg'})

print(r.json())
