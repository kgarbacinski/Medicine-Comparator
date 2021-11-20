import requests

r = requests.get('http://192.168.0.157:5001/equivalents'
             # , json={'name': 'Amlopin 5 mg'})
             , json={'name': '05909990132928'})

print(r)
print(r.json())

