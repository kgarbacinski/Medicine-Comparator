import requests

r = requests.get('http://127.0.0.1:3000/equivalents'
             , json={'ean_or_name': 'Amlozek 5 mg'})

print(r.json())