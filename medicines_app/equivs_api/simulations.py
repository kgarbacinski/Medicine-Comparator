import requests

r = requests.get('http://127.0.0.1:3000/equivalents'
             , json={'name': 'Amlozek 5 mg'})

print(r.json())