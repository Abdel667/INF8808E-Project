
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
        html.H2('2020')
    ]),

    # Main visualization section (always visible)
    html.Div(className='main-viz-section', children=[
        html.H3('Main Visualization'),
        html.P('Summary description for the main visualization goes here.'),
        dcc.Graph(id='main-heatmap', figure={
            "data": [],
            "layout": {"title": "Main Heatmap (Placeholder)"}
        }),
        html.P('Possible interactions: ...')
    ]),

    # Tabs for the three themes
    dcc.Tabs(
        id='theme-tabs',
        value='tab-1',
        children=[
            dcc.Tab(label='Genre Trends and Market Evolution', value='tab-1'),
            dcc.Tab(label='Lyrics and Thematic Analysis', value='tab-2'),
            dcc.Tab(label='Audio & Listener Behavior', value='tab-3'),
        ],
        style={'marginTop': '40px'},
    ),

    html.Div(id='tab-content', style={'marginTop': '20px'})
])

@app.callback(
    Output('tab-content', 'children'),
    [Input('theme-tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Genre Trends and Market Evolution'),
            html.P('Summary description for this section.'),
            html.Ul([
                html.Li('Question 1 targeted by this visualization.'),
                html.Li('Question 2 targeted by this visualization.')
            ]),
            dcc.Graph(id='line-chart', figure={
                "data": [],
                "layout": {"title": "Line Chart (Placeholder)"}
            }),
            html.P('Possible interactions: ...')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Lyrics and Thematic Analysis'),
            html.P('Summary description for this section.'),
            html.Ul([
                html.Li('Question 1 targeted by this visualization.'),
                html.Li('Question 2 targeted by this visualization.')
            ]),
            dcc.Graph(id='histogram', figure={
                "data": [],
                "layout": {"title": "Histogram (Placeholder)"}
            }),
            html.P('Possible interactions: ...')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Audio & Listener Behavior'),
            html.P('Summary description for this section.'),
            html.Ul([
                html.Li('Question 1 targeted by this visualization.'),
                html.Li('Question 2 targeted by this visualization.')
            ]),
            dcc.Graph(id='bar-chart', figure={
                "data": [],
                "layout": {"title": "Bar Chart (Placeholder)"}
            }),
            html.P('Possible interactions: ...')
        ])


