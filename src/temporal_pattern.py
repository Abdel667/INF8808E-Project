import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# === Données ===
df = pd.read_csv("./assets/data/spotify_songs.csv")

# Convert release date column to datetime objects, handling potential errors
df["track_album_release_date"] = pd.to_datetime(
    df["track_album_release_date"], errors="coerce"
)
df.dropna(subset=["track_album_release_date"], inplace=True)

# --- Season Categorization ---
df["release_month"] = df["track_album_release_date"].dt.month


def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"


df["season"] = df["release_month"].apply(get_season)

# --- Create numerical index for seasons and define order ---
season_order = ["Winter", "Spring", "Summer", "Fall"]
season_to_index = {season: i for i, season in enumerate(season_order)}
df["season_index"] = df["season"].map(season_to_index)

# --- Manual Density-Based Y-Jitter Calculation ---

# Parameters for the density-based Y-jitter
BIN_SIZE = 1  # Bin popularity scores into intervals of this size (e.g., 0-1, 1-2, etc.)
JITTER_STEP_Y = (
    0.005  # Vertical distance between stacked points (adjust for visual density)
)
MAX_JITTER_RANGE_Y = (
    0.45  # Maximum vertical displacement from the center of the season band
)

df["custom_y_jitter"] = 0.0  # Initialize custom Y-jitter column

# --- Add X-Jitter Parameters ---
# This is the new part for horizontal jitter
X_JITTER_MAGNITUDE = 0.95  # Total range of horizontal jitter (e.g., -0.25 to +0.25)
np.random.seed(42)  # For reproducibility of random jitter

# Calculate custom Y-jitter
for season in season_order:
    df_season_idx = df["season"] == season
    df_season = df[df_season_idx].copy()

    df_season["popularity_bin"] = (
        np.floor(df_season["track_popularity"] / BIN_SIZE) * BIN_SIZE
    )
    df_season = df_season.sort_values(by="popularity_bin")

    current_bin = None
    stack_counter = 0

    for idx, row in df_season.iterrows():
        if row["popularity_bin"] != current_bin:
            current_bin = row["popularity_bin"]
            stack_counter = 0

        y_offset = (
            (stack_counter // 2 + 1) * JITTER_STEP_Y * (-1 if stack_counter % 2 else 1)
        )
        stack_counter += 1

        if abs(y_offset) > MAX_JITTER_RANGE_Y:
            y_offset = np.sign(y_offset) * MAX_JITTER_RANGE_Y

        df.loc[idx, "custom_y_jitter"] = y_offset

# --- Apply X-Jitter (separate from Y-jitter logic) ---
# We'll apply this to the 'track_popularity' itself to create 'x_plot'
# This X-jitter is typically very small and random to break overlaps for identical X values.
# To ensure points with the exact same popularity score are visible, we add a tiny random x-offset.
# This ensures that points that would otherwise perfectly overlap on the x-axis are slightly separated.
df["custom_x_jitter"] = (np.random.rand(len(df)) - 0.5) * X_JITTER_MAGNITUDE


# Calculate the final plotting coordinates
df["x_plot"] = df["track_popularity"] + df["custom_x_jitter"]
df["y_plot"] = df["season_index"] + df["custom_y_jitter"]

# --- Visualization using go.Scatter ---

fig = go.Figure()

colors_by_season = px.colors.qualitative.Plotly
unique_genres = df["playlist_genre"].unique()
# Create a mapping from genre to color using a robust Plotly palette
# Use a larger palette if you have many genres, e.g., px.colors.qualitative.Alphabet
genre_colors = {
    genre: px.colors.qualitative.Bold[i % len(px.colors.qualitative.Bold)]
    for i, genre in enumerate(unique_genres)
}
color_by_column = "playlist_genre"
# Loop through each unique genre to create separate traces
for genre_name in unique_genres:
    # Filter data for the current genre
    if color_by_column == "season":  # If we fell back to season coloring
        df_genre_filtered = df[df["season"] == genre_name].copy()
    else:  # Normal genre coloring
        df_genre_filtered = df[df["playlist_genre"] == genre_name].copy()

    # Ensure there's data for this genre before adding a trace
    if not df_genre_filtered.empty:
        fig.add_trace(
            go.Scatter(
                x=df_genre_filtered["x_plot"],
                y=df_genre_filtered["y_plot"],
                mode="markers",
                name=genre_name,  # The legend entry will now be the genre name
                marker=dict(
                    size=4,
                    opacity=0.6,
                    color=genre_colors[
                        genre_name
                    ],  # Use the color mapped to this genre
                    line=dict(width=0),
                ),
                hovertemplate=(
                    f"<b>Genre</b>: {genre_name}<br>"  # Display genre in hover
                    + "<b>Season</b>: %{customdata[4]}<br>"  # Add season to customdata
                    + "<b>Popularity</b>: %{x:.2f}<br>"
                    + "<b>Original Pop.</b>: %{customdata[3]}<br>"
                    + "<b>Track</b>: %{customdata[0]}<br>"
                    + "<b>Artist</b>: %{customdata[1]}<br>"
                    + "<b>Release Date</b>: %{customdata[2]|%Y-%m-%d}<extra></extra>"
                ),
                customdata=df_genre_filtered[
                    [
                        "track_name",
                        "track_artist",
                        "track_album_release_date",
                        "track_popularity",
                        "season",
                    ]
                ].values,  # Add 'season' to customdata
                showlegend=True,
            )
        )

# --- Layout and Styling ---
fig.update_layout(
    title="Song Popularity by Release Season & Genre (Manual Jitter)",
    plot_bgcolor="white",
    xaxis=dict(
        title="Track Popularity Score (with slight horizontal jitter)",
        range=[0, 100],
        showgrid=True,
        gridcolor="LightGray",
        zeroline=True,
        zerolinecolor="Gainsboro",
    ),
    yaxis=dict(
        title="Release Season",  # Y-axis still represents seasons, but points are colored by genre
        tickmode="array",
        tickvals=list(season_to_index.values()),
        ticktext=list(season_to_index.keys()),
        showgrid=True,
        gridcolor="LightGray",
        zeroline=True,
        zerolinecolor="Gainsboro",
        range=[-0.5, len(season_order) - 0.5],
    ),
    legend_title_text="Playlist Genre",  # Change legend title
    height=800,
    width=1600,
    font=dict(size=12),
)

fig.show()
