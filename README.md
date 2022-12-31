# Dashboard-Python-Meteo

## User Guide

### Description

Cet application contient un histogramme qui représente le nombre de villes sur un température précis et une carte géographique qui représente la température en temps réel de tous les villes d'un departement.
Et l'utilisateur peut choisir le département pour voir la température de tous les villes dans ce département. 

- Les données de météo viens du site :
https://open-meteo.com/en/docs#api_form

- Les coordonnées géographiques viennent du site: https://geo.api.gouv.fr

### Installation

Pour cloner le projet 

``git clone git@github.com:Ehoky/Dashboard-Python-Meteo.git``

Pour installer l’ensemble des dépendances nécessaires:

``$ python -m pip install -r requirements.tx``

### Démarrage 

Pour lancer cet application:
``$ python main.py``

Et l'application se lance sur l'adresse suivant:

http://127.0.0.1:8050/

### Rapport d'analyse

Nous avons utilisé les données dynamiques via API, ce qui nous permet avoir les données de météo en temps réel. 
Cependant, le démarrage et l'update des données prends du temps, on a fait le choix d'affichier le météo d'un département, cela nous permet de ralentir les demandes à l'API météo pour éviter le bug et aussi pour gaganer un peu plus de temps.
On remarque la température dans un département est homogène. 

### Copyright

Je déclare sur l’honneur que le code fourni a été produit par nous-même.



## Developper Guide
On a séparé notre programme en frontend(app.py) et backend(get_data_for_dashboard et trad_weather_code.py).
Le fichier main.py appelle le frontend pour lancer tous les contenues de l'application. 
Le backend est appelé par le frontend pour avoir tous les data que le frontend a besoin. 

### Architecture du code
```mermaid 

    graph TD
    main-->app.py;
    app-->get_data_for_dashboard.py;
    app-->trad_weather_code.py

    subgraph frontend
        app.py

    subgraph backend
        get_data_for_dashboard
        trad_weather_code
    end
```

### Frontend 
Le frontend a deux fonctions:
get_map(weather):
get_histogram(weather):
app.layout:

app.callback:

### Backend
get_departments():

get_cities_coordinates(num_departement):

get_weather_for_coor(latitude, longitude):


get_weather(num_departement):
main appelle frontend, frontend
backend a deux parties, trad_weather_code (decode_weather)
get data liste departement, commune info, les météo sur les villes 


Explication:
### Architecture du code

-mermaid

-organigramme

-diagramme de classes (si il y a un département)
