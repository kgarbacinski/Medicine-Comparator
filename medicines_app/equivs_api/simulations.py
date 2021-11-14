import requests

r = requests.get('http://192.168.0.134:5001/equivalents'
             , json={'ean_or_name': 'Amlozek 5 mg'})

print(r)
print(r.json())

