import pandas as pd


def load_and_clean_data(filepath="./assets/data/spotify_songs.csv"):
    df = pd.read_csv(filepath)

    # Formatage des dates
    df["year"] = pd.to_datetime(df["track_album_release_date"], errors="coerce").dt.year

    # Nettoyage de colonnes utiles
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
