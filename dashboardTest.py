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
from test import get_cities
from test import get_cities_coordinates
from dash import Input, Output

#
# Data
#

year = 2022 

all_dpt = get_cities()

infos_dpt = {'name':[], 'code':[]}
for dpt in all_dpt:
    infos_dpt['name'].append(dpt['nom'])
    infos_dpt['code'].append(dpt['code'])




#
# Main
#

if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    app.layout = html.Div(children=[

                            html.H1(children=f'Meteo ({year})',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}),
                            html.Div(),
                            # html.Div([
                            #     "Numéro de département: ",
                            #     dcc.Input(id='num_depart', value='75', type='number')
                            #     ]),
                            html.Div(
                                dcc.Dropdown(
                                    infos_dpt['code'],
                                    id='dpt',
                                    # value=infos_dpt['code']
                                )
                            ),
                            html.Iframe(id='map',srcDoc=open('map.html','r').read(),width='100%',height='600' )                   

    ]
    )
    @app.callback(
        Output(component_id='map',component_property='src'),
        Input(component_id='dpt',component_property='value')
        
    )
    def update_dpt(input):
        get_cities_coordinates(input)
        print(input)
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
        return 'map.html'
    #
    # RUN APP
    #

app.run_server(debug=True) # (8)