import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Base de l'url pour accéder aux données des API
weather_api_url = 'https://api.open-meteo.com/v1/forecast'
geo_api_url = 'https://geo.api.gouv.fr'


def get_departments():
    """Renvoie la liste des départements de la France métropolitaines et d'outre-mer"""
    response = requests.get(f'{geo_api_url}/departements')
    if not response.ok:
        print(f"Erreur de connexion {response.status_code} car '{response.reason}'")

    all_dpt = response.json()
    infos_dpt = {'name': [], 'code': []}
    for dpt in all_dpt:
        infos_dpt['name'].append(dpt['nom'])
        infos_dpt['code'].append(dpt['code'])

    return infos_dpt


def get_cities_coordinates(num_departement):
    """Renvoie les données géographiques de toutes les communes du département en paramètre"""
    # requête
    response = requests.get(f'{geo_api_url}/departements/{num_departement}/communes?fields=nom,centre')
    if not response.ok:
        print(f"Erreur de connexion {response.status_code} car '{response.reason}'")

    return response.json()


def get_weather_for_coor(latitude, longitude):
    """Renvoie les données météo pour les données géographiques en paramètres"""
    # Ralentir la quantité d'appel à l'API pour éviter une erreur 'Max retries exceeded with url'
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    # requête
    response = session.get(f'{weather_api_url}?latitude={latitude}&longitude={longitude}&current_weather=true')
    if not response.ok:
        print(f"Erreur de connexion {response.status_code} car '{response.reason}'")

    complete_response = response.json()
    return complete_response['current_weather']


def get_weather(num_departement):
    """Renvoie la météo de toutes les villes du département entré en paramètre"""
    cities = get_cities_coordinates(num_departement)

    current_weather = {'name': [], 'latitude': [], 'longitude': [], 'temperature': [], 'weathercode': []}
    for city in cities:
        city_longitude = city['centre']['coordinates'][0]
        city_latitude = city['centre']['coordinates'][1]

        # Latitude Longitude utilisés pour l'exemple
        current_weather_for_city = get_weather_for_coor(city_latitude, city_longitude)
        current_weather['name'].append(city['nom'])
        current_weather['latitude'].append(city_latitude)
        current_weather['longitude'].append(city_longitude)
        current_weather['temperature'].append(current_weather_for_city['temperature'])
        current_weather['weathercode'].append(current_weather_for_city['weathercode'])

    return current_weather
