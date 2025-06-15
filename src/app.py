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
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import base64
import io

# Enable dynamic callbacks for components rendered per tab
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = 'Project | INF8808'

# === Load and clean data ===
dataframe = pd.read_csv('spotify_songs.csv')
dataframe['year'] = pd.to_datetime(dataframe['track_album_release_date'], errors='coerce').dt.year
dataframe['duration_min'] = dataframe['duration_ms'] / 60000
dataframe = dataframe.dropna(subset=['energy', 'track_popularity', 'playlist_genre'])
all_genres = sorted(dataframe['playlist_genre'].unique())

# === KDE Plot generation (Q12) ===
def generate_kde_image(selected_genres):
    plt.figure(figsize=(12, 6))
    sns.set(style="whitegrid")

    for genre in selected_genres:
        subset = dataframe[dataframe['playlist_genre'] == genre]
        if len(subset) > 10:
            sns.kdeplot(
                data=subset,
                x="energy",
                weights="track_popularity",
                fill=True,
                common_norm=False,
                alpha=0.4,
                linewidth=1.5,
                label=genre
            )

    plt.title("Q12 – How do higher-energy songs perform across genres", fontsize=15)
    plt.xlabel("Energy")
    plt.ylabel("Popularity-weighted density")
    plt.legend(title="Genre", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode()

# === Duration Line Chart for Q9 ===
df_q9 = dataframe.dropna(subset=['year', 'duration_min', 'track_popularity'])
df_q9 = df_q9[df_q9['track_popularity'] >= 60]
df_q9 = df_q9[df_q9['year'] >= 2000]
avg_by_year = df_q9.groupby('year')['duration_min'].mean().reset_index()
fig_q9 = go.Figure()
if not avg_by_year.empty:
    fig_q9.add_trace(go.Scatter(
        x=avg_by_year['year'],
        y=avg_by_year['duration_min'],
        mode='lines+markers',
        line=dict(color='blue'),
        name='Average Duration'
    ))
fig_q9.update_layout(
    title="Q9 – Evolution of Average Duration of Popular Songs (2000–2020)",
    xaxis_title="Year",
    yaxis_title="Average Duration (min)",
    autosize=True,
    height=500
)

# === Danceability vs Tempo Scatter Plot for Q10 & Q11 ===
df_q10 = dataframe.dropna(subset=["danceability", "tempo", "track_popularity", "playlist_genre"])
fig_q10 = px.scatter(
    df_q10,
    x="danceability",
    y="tempo",
    size="track_popularity",
    color="playlist_genre",
    size_max=12,
    opacity=0.6,
    hover_data=["track_name", "track_popularity", "playlist_genre"],
    labels={
        "danceability": "Danceability",
        "tempo": "Tempo (BPM)",
        "track_popularity": "Popularity",
        "playlist_genre": "Genre"
    },
    title="Q10 & Q11 – Danceability vs Tempo and Popularity by Genre"
)
fig_q10.update_layout(autosize=True, height=500)

# === Layout ===
app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Spotify Songs Analysis'),
        html.H2('From 2000 to 2020')
    ]),

    dcc.Tabs(
        id='tabs',
        value='tab-1',
        children=[
            dcc.Tab(label='Heatmap', value='tab-1'),
            dcc.Tab(label='Line Chart', value='tab-2'),
            dcc.Tab(label='Audio & Listener Behavior', value='tab-3'),
            dcc.Tab(label='Bar Chart', value='tab-4'),
            dcc.Tab(label='Scatter Plot', value='tab-5')
        ],
        style={'marginTop': '20px'}
    ),

    html.Div(id='tab-content', style={'marginTop': '20px'})
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
        return html.Div([
            html.H3("Q9 – Duration of Popular Songs (2000–2020)", style={'textAlign': 'center'}),
            dcc.Graph(figure=fig_q9, config={'responsive': True}, style={"height": "500px"}),

            html.H3("Q10 & Q11 – Danceability vs Tempo and Popularity", style={'textAlign': 'center', 'marginTop': '60px'}),
            dcc.Graph(figure=fig_q10, config={'responsive': True}, style={"height": "500px"}),

            html.H3("Q12 – Energy and Popularity by Genre", style={'textAlign': 'center', 'marginTop': '60px'}),
            dcc.Dropdown(
                id='genre-dropdown',
                options=[{"label": genre, "value": genre} for genre in all_genres],
                value=all_genres,
                multi=True,
                style={"width": "60%", "margin": "auto"}
            ),
            dcc.Loading(
                html.Img(id='kde-image', style={"width": "100%", "maxWidth": "1100px", "marginTop": "20px"}),
                type="circle"
            )
        ])
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

@app.callback(
    Output('kde-image', 'src'),
    Input('genre-dropdown', 'value')
)
def update_kde_image(selected_genres):
    if not selected_genres:
        return ""
    return generate_kde_image(selected_genres)

if __name__ == '__main__':
    app.run(debug=True)
