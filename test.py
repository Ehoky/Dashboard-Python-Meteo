import json
import requests

# Base de l'url pour accéder aux données de l'API
api_url = 'https://api.open-meteo.com/v1/forecast'

# Latitude et longitudes obligatoires, à récupérer dans le csv.
# Exemple : Paris
latitude = 48.85
longitude = 2.35


def lecture_json(filename, mode):
    try:
        with open(filename, mode) as f:
            cont_json = json.load(f)
    except FileNotFoundError:
        print("Fichier non trouvé")
    except PermissionError:
        print("Vous n'avez pas les droits")
        
    return cont_json


def get_meteo(latitude, longitude):
    # requête
    response = requests.get(f'{api_url}?latitude={latitude}&longitude={longitude}&current_weather=true')
    if not response.ok:
        print(f"Project -> Erreur de connexion {response.status_code} car '{response.reason}'")
        
    return response.json()
    
villes = lecture_json('villes.json', 'r')

meteo_actuelle_globale = []
for ville in villes:
    latitude_ville = ville['gps_lat']
    longitude_ville = ville['gps_lng']
    
    meteo_actuelle_pour_ville = get_meteo(latitude_ville, longitude_ville)
    #print(meteo_actuelle_pour_ville)
    meteo_actuelle_globale.append(meteo_actuelle_pour_ville)
    
