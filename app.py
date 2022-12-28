from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

from test import get_weather



app = Dash(__name__)


source_info = pd.DataFrame(get_weather())
source_info_grouped = source_info.groupby(['temperature']).count()

# name pour nombre de villes ayant la même température
fig = px.bar(source_info_grouped, y='name')
fig.update_layout( yaxis_title_text='Count')



app.layout = html.Div(children=[
    html.H1(children='Dashboard Météo'),

    html.Div(children='''
        Ici vous pouvez trouver la température des villes de France en temps réel.
    '''),

    dcc.Graph(
        id='Histogramme de la météo',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)