import pandas as pd

def load_and_clean_data(filepath='./assets/data/spotify_songs.csv'):
    df = pd.read_csv(filepath)

    # Formatage des dates
    df['year'] = pd.to_datetime(df['track_album_release_date'], errors='coerce').dt.year

    # Nettoyage de colonnes utiles
    df['duration_min'] = df['duration_ms'] / 60000
    df = df.dropna(subset=['energy', 'track_popularity', 'playlist_genre', 'speechiness'])

    return df
