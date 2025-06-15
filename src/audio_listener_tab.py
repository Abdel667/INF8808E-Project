import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io
from dash import html, dcc, Input, Output

# === Données ===
df = pd.read_csv("./assets/data/spotify_songs.csv")
df['year'] = pd.to_datetime(df['track_album_release_date'], errors='coerce').dt.year
df['duration_min'] = df['duration_ms'] / 60000

# === Q9 ===
df_q9 = df.dropna(subset=['year', 'duration_min', 'track_popularity'])
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
    height=600
)

# === Q10 & Q11 ===
df_q10 = df.dropna(subset=["danceability", "tempo", "track_popularity", "playlist_genre"])
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
    title="Q10 & Q11 – Danceability and Tempo vs Popularity by Genre"
)
fig_q10.update_layout(autosize=True, height=600)

# === Q12 (KDE Plot) ===
df_q12 = df.dropna(subset=['energy', 'track_popularity', 'playlist_genre'])
genres = sorted(df_q12['playlist_genre'].unique())

def generate_kde_plot(selected_genres):
    plt.figure(figsize=(12, 6))
    sns.set(style="whitegrid")

    for genre in selected_genres:
        subset = df_q12[df_q12['playlist_genre'] == genre]
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

    plt.title("Q12 – Energy vs Popularity across Genres", fontsize=15)
    plt.xlabel("Energy")
    plt.ylabel("Popularity-weighted density")
    plt.legend(title="Genre", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode()

# === Content for Tab 3 ===
def get_audio_listener_content():
    return html.Div([
        html.H3('Audio & Listener Behavior'),
        html.P('This section explores how audio features relate to listener trends.'),

        html.H4("Q9 – Evolution of Duration of Popular Songs"),
        dcc.Graph(figure=fig_q9, config={'responsive': True}, style={"height": "600px"}),

        html.H4("Q10 & Q11 – Danceability and Tempo vs Popularity by Genre"),
        dcc.Graph(figure=fig_q10, config={'responsive': True}, style={"height": "600px"}),

        html.H4("Q12 – Energy vs Popularity across Genres"),
        dcc.Dropdown(
            id='genre-dropdown',
            options=[{"label": genre, "value": genre} for genre in genres],
            value=genres,
            multi=True,
            style={"width": "60%", "margin": "auto"}
        ),
        html.Img(id='kde-image', style={"width": "100%", "maxWidth": "1100px", "marginTop": "20px"})
    ])

# === Register callback (to be called from app.py)
def register_callbacks(app):
    @app.callback(
        Output('kde-image', 'src'),
        Input('genre-dropdown', 'value')
    )
    def update_kde_image(selected_genres):
        if not selected_genres:
            return ""
        return generate_kde_plot(selected_genres)
