from dash import Dash, html, dcc
from dash import Input, Output
import plotly.express as px
import pandas as pd
import folium
import branca.colormap as cm

from get_data_for_dashboard import get_weather, get_departments
from trad_weather_code import decode_weather

app = Dash(__name__)
dpt_information = get_departments()
first_value = get_weather('01')

linear = cm.LinearColormap(
    ['blue', 'yellow', 'orange', 'red'],
    vmin=-20, vmax=40,
    caption='Color Scale for Map'  # Caption for Color scale or Legend
)


def get_histogram(weather):
    """Renvoie un histogramme du nombre de villes ayant une même température"""
    source_info = pd.DataFrame(weather)
    source_info_grouped = source_info.groupby(['temperature']).count()

    # name pour nombre de villes ayant la même température
    fig = px.bar(source_info_grouped, y='name')
    fig.update_layout(yaxis_title_text='Nombre de villes')
    return fig


def get_map(weather):
    """Renvoie une carte qui représente la température et la météo de chaque ville"""
    cities = weather['name']
    lats = weather['latitude']
    longs = weather['longitude']
    temperature = weather['temperature']
    climate = decode_weather(weather)
    weather_map = folium.Map(location=(lats[0], longs[0]), tiles='OpenStreetMap', zoom_start=9)
    # zoom 13 pour voir la carte pour la view d'un departement, zoom 6 pour la carte view toute la france

    for i in range(len(cities)):
        folium.CircleMarker(
            location=(lats[i], longs[i]),
            radius=5,
            color=linear(temperature[i]),
            fill=True,
            tooltip=climate[i],
            popup=temperature[i],
            fill_color=linear(temperature[i]),
        ).add_to(weather_map)
    linear.add_to(weather_map)
    weather_map.save("map.html")
    return open('map.html', 'r').read()


app.layout = html.Div(children=[
    html.H1(children='Dashboard Météo',
            style={'textAlign': 'center', 'color': '#DC143C'}),

    html.Div(children='''
        Ici vous pouvez trouver la température et le météo des villes de France en temps réel.
    '''),

    html.H2(children='Choisissez le département de votre choix',
            style={'textAlign': 'left', 'color': '#7FDBFF'}),

    html.Div(
        dcc.Dropdown(
            dpt_information['code'],
            id='dpt',
            value=dpt_information['code'][0]
        )
    ),

    html.H2(children='Nombre de villes en fonction de la température',
            style={'textAlign': 'left', 'color': '#7FDBFF'}),

    dcc.Graph(
        id='histogram',
        figure=get_histogram(first_value)
    ),

    html.H2(children='Météo et température des communes',
            style={'textAlign': 'left', 'color': '#7FDBFF'}),

    html.Iframe(id='map', srcDoc=get_map(first_value), width='100%', height='600')
])


@app.callback(
    Output('map', 'srcDoc'),
    Output('histogram', 'figure'),
    Input('dpt', 'value')
)
def update(dpt):
    """Met à jour la carte et l'histogramme en fonction du département choisi par l'utilisateur"""
    weather = get_weather(dpt)
    return get_map(weather), get_histogram(weather)
