import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# === Données ===
df = pd.read_csv("./assets/data/spotify_songs.csv")
df["year"] = pd.to_datetime(df["track_album_release_date"], errors="coerce").dt.year
df["duration_min"] = df["duration_ms"] / 60000

# === Q9 ===
df_q9 = df.dropna(subset=["year", "duration_min", "track_popularity"])
df_q9 = df_q9[df_q9["track_popularity"] >= 60]
df_q9 = df_q9[df_q9["year"] >= 2000]
avg_by_year = df_q9.groupby("year")["duration_min"].mean().reset_index()
fig_q9 = go.Figure()
if not avg_by_year.empty:
    fig_q9.add_trace(
        go.Scatter(
            x=avg_by_year["year"],
            y=avg_by_year["duration_min"],
            mode="lines+markers",
            line=dict(color="blue"),
            name="Average Duration",
        )
    )
fig_q9.update_layout(
    title="9 – Evolution of Average Duration of Popular Songs over 20 years (2000–2020)",
    xaxis_title="Year",
    yaxis_title="Average Duration (min)",
    autosize=True,
    height=600,
)

# === Q10 & Q11 ===
df_q10 = df.dropna(
    subset=["danceability", "tempo", "track_popularity", "playlist_genre"]
)
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
        "playlist_genre": "Genre",
    },
    title="10 & 11 – How does Danceability and Tempo influence Popularity by Genre",
)
fig_q10.update_layout(autosize=True, height=600)

# === Q12 – Lissage manuel (style KDE) sans scipy ===
df_q12 = df.dropna(subset=["energy", "track_popularity", "playlist_genre"])
genres = sorted(df_q12["playlist_genre"].unique())


def generate_energy_distribution(selected_genres):
    fig = go.Figure()

    for genre in selected_genres:
        subset = df_q12[df_q12["playlist_genre"] == genre]
        if len(subset) > 10:
            x = subset["energy"].values
            w = subset["track_popularity"].values

            # Histogramme pondéré
            hist, bin_edges = np.histogram(
                x, bins=50, range=(0, 1), weights=w, density=True
            )
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

            # Lissage simple par convolution (fausse KDE)
            smoothed = np.convolve(hist, np.ones(5) / 5, mode="same")

            fig.add_trace(
                go.Scatter(
                    x=bin_centers,
                    y=smoothed,
                    mode="lines",
                    fill="tozeroy",
                    name=genre,
                    opacity=0.5,
                )
            )

    fig.update_layout(
        title="Q12 – Energy influence over Popularity across Genres",
        xaxis_title="Energy",
        yaxis_title="Popularity-weighted density",
        height=600,
    )
    return fig


# === Layout & Callbacks pour Tab 3 ===
def get_audio_listener_content():
    return html.Div(
        [
            html.H3("Duration of Popular Songs (2000–2020)"),
            dcc.Graph(
                figure=fig_q9, config={"responsive": True}, style={"height": "600px"}
            ),
            html.H3("Danceability and Tempo vs Popularity"),
            dcc.Graph(
                figure=fig_q10, config={"responsive": True}, style={"height": "600px"}
            ),
            html.H3("Energy KDE-style by Genre"),
            dcc.Dropdown(
                id="genre-dropdown",
                options=[{"label": genre, "value": genre} for genre in genres],
                value=genres,
                multi=True,
                style={"width": "60%", "margin": "auto"},
            ),
            dcc.Graph(
                id="energy-distribution-graph",
                style={"height": "600px", "marginTop": "20px"},
            ),
        ]
    )


def register_callbacks(app):
    @app.callback(
        Output("energy-distribution-graph", "figure"),
        [Input("genre-dropdown", "value")],
    )
    def update_energy_distribution(selected_genres):
        if not selected_genres:
            return go.Figure()
        return generate_energy_distribution(selected_genres)
