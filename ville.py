import json
import requests

with open('coucou.json', 'w') as f:
    json.dump(requests.get('https://geo.api.gouv.fr/communes?fields=nom,centre').json(), f)