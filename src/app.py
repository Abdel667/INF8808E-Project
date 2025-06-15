
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Team 11 - 
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd


app = dash.Dash(__name__)
app.title = 'Project | INF8808'

dataframe = pd.read_csv('./assets/data/spotify_songs.csv')

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Spotify Songs Analysis'),
        html.H2('From 2010 to 2020')
    ]),
    
    # Tabs at the top
    dcc.Tabs(
        id='tabs',
        value='tab-1',
        children=[
            dcc.Tab(label='Heatmap', value='tab-1'),
            dcc.Tab(label='Line Chart', value='tab-2'),
            dcc.Tab(label='Histogram', value='tab-3'),
            dcc.Tab(label='Bar Chart', value='tab-4'),
            dcc.Tab(label='Scatter Plot', value='tab-5')
        ],
        style={'marginTop': '20px'},  # Space between header and tabs
    ),

    html.Div(id='tab-content', style={'marginTop': '20px'})  # Space between tabs and graph
])

@app.callback(
    Output('tab-content', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab-1':
        return dcc.Graph(id='heatmap', figure={
            "data": [],
            "layout": {"title": "Heatmap (Placeholder)"}
        })
    elif tab == 'tab-2':
        return dcc.Graph(id='line-chart', figure={
            "data": [],
            "layout": {"title": "Line Chart (Placeholder)"}
        })
    elif tab == 'tab-3':
        return dcc.Graph(id='histogram', figure={
            "data": [],
            "layout": {"title": "Histogram (Placeholder)"}
        })
    elif tab == 'tab-4':
        return dcc.Graph(id='bar-chart', figure={
            "data": [],
            "layout": {"title": "Bar Chart (Placeholder)"}
        })
    elif tab == 'tab-5':
        return dcc.Graph(id='scatter-plot', figure={
            "data": [],
            "layout": {"title": "Scatter Plot (Placeholder)"}
        })


