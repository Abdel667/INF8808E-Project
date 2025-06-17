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
from genre_trends_tab import get_genre_trends_content, register_genre_trends_callbacks
from main_visualization import get_main_visualization_content
from preprocess import load_and_clean_data, calculate_custom_jitter

app = dash.Dash(__name__)
app.title = "Project | INF8808"

dataframe = pd.read_csv("./assets/data/spotify_songs.csv")
df = load_and_clean_data()

app.layout = html.Div(
    className="content",
    children=[
        html.Header(
            children=[
                html.H1(
                    "Spotify Songs Analysis",
                    style={
                        "textAlign": "center",
                        "color": "#1DB954",
                        "marginBottom": "10px",
                        "fontFamily": "Arial, sans-serif",
                    },
                ),
                html.H2(
                    "Music Trends & Market Intelligence",
                    style={
                        "textAlign": "center",
                        "color": "#666",
                        "fontWeight": "normal",
                        "fontSize": "18px",
                        "marginBottom": "30px",
                    },
                ),
            ],
            style={
                "backgroundColor": "#191414",
                "padding": "30px 20px",
                "marginBottom": "30px",
            },
        ),
        html.Div(
            className="main-viz-section",
            children=[get_main_visualization_content()],
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "marginBottom": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
            },
        ),
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
            colors={"border": "#1DB954", "primary": "#1DB954", "background": "#f8f9fa"},
        ),
        html.Div(id="tab-content", style={"marginTop": "20px"}),
    ],
    style={
        "backgroundColor": "#f5f5f5",
        "minHeight": "100vh",
        "fontFamily": "Arial, sans-serif",
    },
)

jittered_df = calculate_custom_jitter(df)
tab_4_fig = get_temporal_pattern_content(jittered_df)


@app.callback(Output("tab-content", "children"), [Input("theme-tabs", "value")])
def render_content(tab):
    if tab == "tab-1":
        return get_genre_trends_content()
    elif tab == "tab-2":
        return html.Div(
            [
                html.H3("Lyrics and Thematic Analysis"),
                html.P(
                    "This section explores lyrics and vocal styles via speechiness levels."
                ),
                html.Ul(
                    [
                        html.Li(
                            "How has the average speechiness of top-performing tracks evolved over the last 20 years? "
                        ),
                        html.Li(
                            "Do more popular songs tend to have lower or higher speechiness on average?"
                        ),
                    ]
                ),
                html.H4(" Speechiness Distribution in Popular vs. Less Popular Songs"),
                html.P(
                    "These side-by-side waffle charts illustrate how speechiness levels "
                    "are distributed among songs with different popularity levels. Each chart "
                    "represents 100% of songs using 100 squares."
                ),
                html.Ul(
                    [
                        html.Li(" Low (0.0-0.2): Mostly melodic or instrumental"),
                        html.Li(
                            " Medium (0.2-0.5): Balanced between singing and speaking"
                        ),
                        html.Li(" High (0.5-1.0): Strong spoken-word characteristics"),
                    ]
                ),
                html.P(
                    "In popular songs (popularity > 60), high speechiness is often dominant, "
                    "while less popular songs tend to have lower or medium speechiness levels."
                ),
                get_waffle_content(),
                get_speechiness_line_chart_content(dataframe),
            ],
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
            },
        )
    elif tab == "tab-3":
        return html.Div(
            children=[get_audio_listener_content()],
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
            },
        )
    elif tab == "tab-4":
        return html.Div(
            [
                html.H3("Temporal Pattern of Song Popularity"),
                dcc.Graph(
                    id="temporal-pattern-graph",
                    figure=tab_4_fig,
                    config={"responsive": True},
                    style={
                        "height": "800px",
                        "width": "1600px",
                    },
                ),
            ],
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
            },
        )


register_callbacks(app)  # Tab 3
register_genre_trends_callbacks(app)  # Tab 1

if __name__ == "__main__":
    app.run_server(debug=True)
