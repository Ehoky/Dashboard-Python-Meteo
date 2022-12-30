from dash import Dash, html, dcc
from dash import Input, Output
import plotly.express as px
import pandas as pd
import folium

from get_data_for_dashboard import get_weather, get_departments

app = Dash(__name__)
dpt_information = get_departments()
first_value = get_weather('01')


def get_histogram(weather):
    source_info = pd.DataFrame(weather)
    source_info_grouped = source_info.groupby(['temperature']).count()

    # name pour nombre de villes ayant la même température
    fig = px.bar(source_info_grouped, y='name')
    fig.update_layout(yaxis_title_text='Nombre de villes')
    return fig


def get_map(weather):
    cities = weather['name']
    lats = weather['latitude']
    longs = weather['longitude']
    temperature = weather['temperature']

    weather_map = folium.Map(location=(lats[0], longs[0]), tiles='OpenStreetMap', zoom_start=9)
    # zoom 13 pour voir la carte pour la view d'un departement, zoom 6 pour la carte view toute la france

    for i in range(len(cities)):
        folium.CircleMarker(
            location=(lats[i], longs[i]),
            radius=5,
            color='crimson',
            fill=True,
            popup=temperature[i],
            fill_color='crimson'
        ).add_to(weather_map)

    weather_map.save("map.html")
    return open('map.html', 'r').read()


app.layout = html.Div(children=[
    html.H1(children='Dashboard Météo',
            style={'textAlign': 'center', 'color': '#7FDBFF'}),

    html.Div(children='''
        Ici vous pouvez trouver la température des villes de France en temps réel.
    '''),

    html.Div(
        dcc.Dropdown(
            dpt_information['code'],
            id='dpt',
            value=dpt_information['code'][0]
        )
    ),

    dcc.Graph(
        id='histogram',
        figure=get_histogram(first_value)
    ),

    html.Iframe(id='map', srcDoc=get_map(first_value), width='100%', height='600')
])


@app.callback(
    Output('map', 'srcDoc'),
    Output('histogram', 'figure'),
    Input('dpt', 'value')
)
def update(dpt):
    weather = get_weather(dpt)
    return get_map(weather), get_histogram(weather)
