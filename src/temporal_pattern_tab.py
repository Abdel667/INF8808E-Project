import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

SEASON_ORDER = ["Winter", "Spring", "Summer", "Fall"]

BIN_SIZE = 1
JITTER_STEP_Y = 0.005
MAX_JITTER_RANGE_Y = 0.45
X_JITTER_MAGNITUDE = 0.95
NP_RANDOM_SEED = 42

SEASON_TO_INDEX = {season: i for i, season in enumerate(SEASON_ORDER)}

np.random.seed(NP_RANDOM_SEED)


def compute_plot_positions(df_with_jitter: pd.DataFrame) -> pd.DataFrame:
    df_with_jitter["custom_x_jitter"] = (
        np.random.rand(len(df_with_jitter)) - 0.5
    ) * X_JITTER_MAGNITUDE

    df_with_jitter["x_plot"] = (
        df_with_jitter["track_popularity"] + df_with_jitter["custom_x_jitter"]
    )
    df_with_jitter["y_plot"] = (
        df_with_jitter["season"].map(SEASON_TO_INDEX)
        + df_with_jitter["custom_y_jitter"]
    )

    return df_with_jitter


def get_temporal_pattern_content(df: pd.DataFrame):
    print("what")
    df_plot_ready = compute_plot_positions(df)
    print("what")

    fig = go.Figure()

    color_by_column = "playlist_genre"
    unique_color_categories = df_plot_ready[color_by_column].unique()
    color_map = {
        category: px.colors.qualitative.Bold[i % len(px.colors.qualitative.Bold)]
        for i, category in enumerate(unique_color_categories)
    }
    legend_title = "Genre"

    for category_name in unique_color_categories:
        df_filtered = df_plot_ready[
            df_plot_ready[color_by_column] == category_name
        ].copy()

        if not df_filtered.empty:
            fig.add_trace(
                go.Scatter(
                    x=df_filtered["x_plot"],
                    y=df_filtered["y_plot"],
                    mode="markers",
                    name=category_name,
                    marker=dict(
                        size=4,
                        opacity=0.6,
                        color=color_map[category_name],
                        line=dict(width=0),
                    ),
                    hovertemplate=(
                        f"<b>{legend_title.replace(' ', '')}</b>: {category_name}<br>"
                        + "<b>Season</b>: %{customdata[4]}<br>"
                        + "<b>Popularity</b>: %{x:.2f}<br>"
                        + "<b>Track</b>: %{customdata[0]}<br>"
                        + "<b>Artist</b>: %{customdata[1]}<br>"
                        + "<b>Release Date</b>: %{customdata[2]|%Y-%m-%d}<extra></extra>"
                    ),
                    customdata=df_filtered[
                        [
                            "track_name",
                            "track_artist",
                            "track_album_release_date",
                            "track_popularity",
                            "season",
                        ]
                    ].values,
                    showlegend=True,
                )
            )

    print("done")
    fig.update_layout(
        title="Song Popularity by Release Season & Genre",
        plot_bgcolor="white",
        xaxis=dict(
            title="Track Popularity Score",
            range=[0, 100],
            showgrid=True,
            gridcolor="LightGray",
            zeroline=True,
            zerolinecolor="Gainsboro",
        ),
        yaxis=dict(
            title="Release Season",
            tickmode="array",
            tickvals=list(SEASON_TO_INDEX.values()),
            ticktext=list(SEASON_TO_INDEX.keys()),
            showgrid=True,
            gridcolor="LightGray",
            zeroline=True,
            zerolinecolor="Gainsboro",
            range=[-0.5, len(SEASON_ORDER) - 0.5],
        ),
        legend_title_text=legend_title,
        height=800,
        width=1600,
        font=dict(size=12),
    )

    print("done")
    return fig
