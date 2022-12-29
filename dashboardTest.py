# filename = 'dash-01.py'

#
# Imports
#
import folium
from folium import GeoJson

import plotly_express as px

import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from test import get_weather

#
# Data
#

year = 2022 


df = px.data.election()
current_weather= get_weather()
cities=current_weather['name']
lats=current_weather['latitude']
longs=current_weather['longitude']
temperature=current_weather['temperature']

map = folium.Map(location=(longs[0],lats[0]),tiles='OpenStreetMap', zoom_start=13)
#zoom 13 pour voir la carte pour la view d'un departement, zoom 6 pour la carte view toute la france


for i in range(len(cities)):
    folium.CircleMarker(
        location = (longs[i],lats[i]),
        radius = 15,
        color = 'crimson',
        fill = True,
        popup=temperature[i],
        fill_color = 'crimson'
    ).add_to(map)
    
map.save(outfile='map.html')

# villes = json.load('villes.json')

#
# Main
#

if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    
    fig1 = px.choropleth_mapbox(zoom=9) #map function
    

    app.layout = html.Div(children=[

                            html.H1(children=f'Meteo ({year})',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                            html.Iframe(id='map',srcDoc=open('map.html','r').read(),width='100%',height='600' )                   

    ]
    )

    #
    # RUN APP
    #

    app.run_server(debug=True) # (8)