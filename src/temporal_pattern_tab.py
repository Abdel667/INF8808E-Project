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


def _calculate_custom_y_jitter(df: pd.DataFrame) -> pd.DataFrame:
    df_with_jitter = df.copy()
    df_with_jitter["custom_y_jitter"] = 0.0

    for season in SEASON_ORDER:
        df_season_idx = df_with_jitter["season"] == season
        df_season = df_with_jitter[df_season_idx].copy()

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
                (stack_counter // 2 + 1)
                * JITTER_STEP_Y
                * (-1 if stack_counter % 2 else 1)
            )
            stack_counter += 1

            if abs(y_offset) > MAX_JITTER_RANGE_Y:
                y_offset = np.sign(y_offset) * MAX_JITTER_RANGE_Y

            df_with_jitter.loc[idx, "custom_y_jitter"] = y_offset

    return df_with_jitter


def _compute_plot_positions(df: pd.DataFrame) -> pd.DataFrame:
    df_with_jitter = _calculate_custom_y_jitter(df)

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
    df_plot_ready = _compute_plot_positions(df)

    fig = go.Figure()

    color_by_column = "playlist_genre"
    unique_color_categories = df_plot_ready[color_by_column].unique()
    color_map = {
        category: px.colors.qualitative.Bold[i % len(px.colors.qualitative.Bold)]
        for i, category in enumerate(unique_color_categories)
    }
    legend_title = "Playlist Genre"

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
                        + "<b>Original Pop.</b>: %{customdata[3]}<br>"
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

    fig.update_layout(
        title="Song Popularity by Release Season & Genre (Manual Jitter)",
        plot_bgcolor="white",
        xaxis=dict(
            title="Track Popularity Score (no horizontal jitter for now)",
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

    return fig
