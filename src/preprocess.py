import pandas as pd
import numpy as np

SEASON_ORDER = ["Winter", "Spring", "Summer", "Fall"]

BIN_SIZE = 1
JITTER_STEP_Y = 0.005
MAX_JITTER_RANGE_Y = 0.45
X_JITTER_MAGNITUDE = 0.95
NP_RANDOM_SEED = 69
MAX_SONG_TRESHOLD = 100
np.random.seed(NP_RANDOM_SEED)


def load_and_clean_data(filepath="./assets/data/spotify_songs.csv"):
    df = pd.read_csv(filepath)

    df["year"] = pd.to_datetime(df["track_album_release_date"], errors="coerce").dt.year

    df["duration_min"] = df["duration_ms"] / 60000
    df = df.dropna(
        subset=["energy", "track_popularity", "playlist_genre", "speechiness"]
    )
    df = _add_season_collumn(df)

    return df


def _add_season_collumn(df):
    df["track_album_release_date"] = pd.to_datetime(
        df["track_album_release_date"], errors="coerce"
    )
    df.dropna(subset=["track_album_release_date"], inplace=True)

    df["release_month"] = df["track_album_release_date"].dt.month

    df["season"] = df["release_month"].apply(
        lambda month: "Winter"
        if month in [12, 1, 2]
        else "Spring"
        if month in [3, 4, 5]
        else "Summer"
        if month in [6, 7, 8]
        else "Fall"
    )
    return df


def create_popularity_density_map(df: pd.DataFrame) -> dict:
    density_counts = (
        df.groupby(["season", "track_popularity"]).size().reset_index(name="count")
    )

    density_map = {}
    for _, row in density_counts.iterrows():
        season = row["season"]
        popularity = row["track_popularity"]
        count = row["count"]

        density = min(count / MAX_SONG_TRESHOLD, 1.0)
        density_map[(season, popularity)] = density

    return density_map


def calculate_custom_jitter(df: pd.DataFrame) -> pd.DataFrame:
    df_with_jitter = df.copy()

    density_map = create_popularity_density_map(df)

    jitter_factors = np.random.rand(len(df_with_jitter))

    def get_density(season, popularity):
        return density_map.get((season, popularity), 0.0)

    densities = np.array(
        [
            get_density(season, popularity)
            for season, popularity in zip(
                df_with_jitter["season"], df_with_jitter["track_popularity"]
            )
        ]
    )

    alternating_signs = np.where(np.arange(len(df_with_jitter)) % 2 == 0, 1, -1)

    y_offsets = densities * jitter_factors * MAX_JITTER_RANGE_Y * alternating_signs

    df_with_jitter["custom_y_jitter"] = y_offsets

    return df_with_jitter
