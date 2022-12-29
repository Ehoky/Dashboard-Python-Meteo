import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Base de l'url pour accéder aux données de l'API
api_url = 'https://api.open-meteo.com/v1/forecast'


def get_cities():
    response = requests.get(f'https://geo.api.gouv.fr/departements')
    if not response.ok:
        print(f"Erreur de connexion {response.status_code} car '{response.reason}'")
    
    return response.json()


def get_cities_coordinates(num_departement):
    # requête
    response = requests.get(f'https://geo.api.gouv.fr/departements/{num_departement}/communes?fields=nom,centre')
    if not response.ok:
        print(f"Erreur de connexion {response.status_code} car '{response.reason}'")
    
    return response.json()


def get_weather_for_coor(latitude, longitude):
    # Ralentir la quantité d'appel à l'API pour éviter une erreur 'Max retries exceeded with url'
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    # requête
    response = session.get(f'{api_url}?latitude={latitude}&longitude={longitude}&current_weather=true')
    if not response.ok:
        print(f"Erreur de connexion {response.status_code} car '{response.reason}'")
    
    complete_response = response.json()
    return complete_response['current_weather']


def get_weather(n_dpt):
    cities = get_cities_coordinates(n_dpt)
    
    current_weather = {'name':[], 'latitude':[], 'longitude':[], 'temperature':[], 'weathercode':[]}
    for city in cities:
        city_latitude = city['centre']['coordinates'][0]
        city_longitude = city['centre']['coordinates'][1]
        
        # Latitude Longitude utilisés pour l'exemple
        current_weather_for_city = get_weather_for_coor(city_latitude, city_longitude)
        current_weather['name'].append(city['nom'])
        current_weather['latitude'].append(city_latitude)
        current_weather['longitude'].append(city_longitude)
        current_weather['temperature'].append(current_weather_for_city['temperature'])
        current_weather['weathercode'].append(current_weather_for_city['weathercode'])
        # Enregistrement à modifier : faire des listes dans 1 dictionnaire unique
        
    return current_weather
        

#print(get_weather())