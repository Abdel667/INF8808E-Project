# -*- coding: utf-8 -*-
"""
File name: app.py
Author: Team 11 -
Course: INF8808
Python Version: 3.8

This file is the entry point for our dash app.
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd

from speechiness_line_chart import get_speechiness_line_chart_content
from waffle_content import get_waffle_content
from audio_listener_tab import get_audio_listener_content, register_callbacks
from temporal_pattern_tab import get_temporal_pattern_content
from preprocess import load_and_clean_data

app = dash.Dash(__name__)
app.title = "Project | INF8808"

dataframe = pd.read_csv("./assets/data/spotify_songs.csv")
df = load_and_clean_data()

app.layout = html.Div(
    className="content",
    children=[
        html.Header(children=[html.H1("Spotify Songs Analysis"), html.H2("2020")]),
        # Main visualization section (always visible)
        html.Div(
            className="main-viz-section",
            children=[
                html.H3("Main Visualization"),
                html.P("Summary description for the main visualization goes here."),
                dcc.Graph(
                    id="main-heatmap",
                    figure={
                        "data": [],
                        "layout": {"title": "Main Heatmap (Placeholder)"},
                    },
                ),
                html.P("Possible interactions: ..."),
            ],
        ),
        # Tabs for the three themes
        dcc.Tabs(
            id="theme-tabs",
            value="tab-1",
            children=[
                dcc.Tab(label="Genre Trends and Market Evolution", value="tab-1"),
                dcc.Tab(label="Lyrics and Thematic Analysis", value="tab-2"),
                dcc.Tab(label="Audio & Listener Behavior", value="tab-3"),
                dcc.Tab(label="Temporal Pattern", value="tab-4"),
            ],
            style={"marginTop": "40px"},
        ),
        html.Div(id="tab-content", style={"marginTop": "20px"}),
    ],
)


@app.callback(Output("tab-content", "children"), [Input("theme-tabs", "value")])
def render_content(tab):
    if tab == "tab-1":
        return html.Div(
            [
                html.H3("Genre Trends and Market Evolution"),
                html.P("Summary description for this section."),
                html.Ul(
                    [
                        html.Li("Question 1 targeted by this visualization."),
                        html.Li("Question 2 targeted by this visualization."),
                    ]
                ),
                dcc.Graph(
                    id="line-chart",
                    figure={
                        "data": [],
                        "layout": {"title": "Line Chart (Placeholder)"},
                    },
                ),
                html.P("Possible interactions: ..."),
            ]
        )
    elif tab == "tab-2":
        return html.Div(
            [
                html.H3("Lyrics and Thematic Analysis"),
                html.P(
                    "This section explores lyrics and vocal styles via speechiness levels."
                ),
                html.Ul(
                [
                    html.Li("How has the average speechiness of top-performing tracks evolved over the last 20 years? "),
                    html.Li("Do more popular songs tend to have lower or higher speechiness on average?"),
                ]
            ),

            html.H4(" Speechiness Distribution in Popular vs. Less Popular Songs"),
            html.P(
                "These side-by-side waffle charts illustrate how speechiness levels "
                "are distributed among songs with different popularity levels. Each chart "
                "represents 100% of songs using 100 squares."
            ),
            html.Ul([
                html.Li(" Low (0.0-0.2): Mostly melodic or instrumental"),
                html.Li(" Medium (0.2-0.5): Balanced between singing and speaking"),
                html.Li(" High (0.5-1.0): Strong spoken-word characteristics")
            ]),
            html.P(
                "In popular songs (popularity > 60), high speechiness is often dominant, "
                "while less popular songs tend to have lower or medium speechiness levels."
            ),
                get_waffle_content(),
                get_speechiness_line_chart_content(dataframe),
            ]
        )
    elif tab == "tab-3":
        return get_audio_listener_content()
    elif tab == "tab-4":
        return html.Div(
            [
                html.H3("Temporal Pattern of Song Popularity"),
                html.P(
                    "This plot visualizes song popularity across seasons, with points colored by genre. Vertical jitter represents density within popularity bins, and horizontal jitter separates exact duplicates."
                ),
                dcc.Graph(
                    id="temporal-pattern-graph",
                    figure=get_temporal_pattern_content(df),
                    config={"responsive": True},
                    style={
                        "height": "800px",
                        "width": "1600px",
                    },
                ),
                html.P(
                    "Possible interactions: Hover over points for song details. Note the density distribution for different genres across seasons."
                ),
            ]
        )


# Enregistre les callbacks dynamiques (Q12)
register_callbacks(app)
