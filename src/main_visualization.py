import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash_core_components as dcc
import dash_html_components as html


def load_main_data():
    """Load and preprocess data for main visualization"""
    df = pd.read_csv("./assets/data/spotify_songs.csv")
    df["track_album_release_date"] = pd.to_datetime(
        df["track_album_release_date"], errors="coerce"
    )
    df["year"] = df["track_album_release_date"].dt.year

    # Clean data
    df = df.dropna(subset=["year", "track_popularity", "playlist_genre"])
    df = df[df["year"] >= 1960]  # Keep broader range for main viz

    return df


def calculate_kpis(df):
    """Calculate key performance indicators"""
    total_songs = len(df)
    total_artists = df["track_artist"].nunique()
    total_genres = df["playlist_genre"].nunique()
    total_subgenres = df["playlist_subgenre"].nunique()
    year_range = f"{int(df['year'].min())}-{int(df['year'].max())}"
    avg_popularity = df["track_popularity"].mean()

    return {
        "total_songs": total_songs,
        "total_artists": total_artists,
        "total_genres": total_genres,
        "total_subgenres": total_subgenres,
        "year_range": year_range,
        "avg_popularity": avg_popularity,
    }


def create_kpi_cards(kpis):
    """Create KPI cards display"""
    return html.Div(
        [
            html.Div(
                [
                    html.H3(
                        f"{kpis['total_songs']:,}",
                        style={"color": "#2E86AB", "margin": "0"},
                    ),
                    html.P("Total Songs", style={"margin": "0", "fontSize": "14px"}),
                ],
                className="kpi-card",
                style={
                    "textAlign": "center",
                    "padding": "20px",
                    "backgroundColor": "#f8f9fa",
                    "borderRadius": "8px",
                    "margin": "10px",
                    "minWidth": "120px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                },
            ),
            html.Div(
                [
                    html.H3(
                        f"{kpis['total_artists']:,}",
                        style={"color": "#A23B72", "margin": "0"},
                    ),
                    html.P("Unique Artists", style={"margin": "0", "fontSize": "14px"}),
                ],
                className="kpi-card",
                style={
                    "textAlign": "center",
                    "padding": "20px",
                    "backgroundColor": "#f8f9fa",
                    "borderRadius": "8px",
                    "margin": "10px",
                    "minWidth": "120px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                },
            ),
            html.Div(
                [
                    html.H3(
                        f"{kpis['total_genres']}",
                        style={"color": "#F18F01", "margin": "0"},
                    ),
                    html.P("Main Genres", style={"margin": "0", "fontSize": "14px"}),
                ],
                className="kpi-card",
                style={
                    "textAlign": "center",
                    "padding": "20px",
                    "backgroundColor": "#f8f9fa",
                    "borderRadius": "8px",
                    "margin": "10px",
                    "minWidth": "120px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                },
            ),
            html.Div(
                [
                    html.H3(
                        f"{kpis['total_subgenres']}",
                        style={"color": "#C73E1D", "margin": "0"},
                    ),
                    html.P("Subgenres", style={"margin": "0", "fontSize": "14px"}),
                ],
                className="kpi-card",
                style={
                    "textAlign": "center",
                    "padding": "20px",
                    "backgroundColor": "#f8f9fa",
                    "borderRadius": "8px",
                    "margin": "10px",
                    "minWidth": "120px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                },
            ),
            html.Div(
                [
                    html.H3(
                        kpis["year_range"], style={"color": "#2E86AB", "margin": "0"}
                    ),
                    html.P("Year Range", style={"margin": "0", "fontSize": "14px"}),
                ],
                className="kpi-card",
                style={
                    "textAlign": "center",
                    "padding": "20px",
                    "backgroundColor": "#f8f9fa",
                    "borderRadius": "8px",
                    "margin": "10px",
                    "minWidth": "120px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                },
            ),
            html.Div(
                [
                    html.H3(
                        f"{kpis['avg_popularity']:.1f}",
                        style={"color": "#A23B72", "margin": "0"},
                    ),
                    html.P("Avg Popularity", style={"margin": "0", "fontSize": "14px"}),
                ],
                className="kpi-card",
                style={
                    "textAlign": "center",
                    "padding": "20px",
                    "backgroundColor": "#f8f9fa",
                    "borderRadius": "8px",
                    "margin": "10px",
                    "minWidth": "120px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                },
            ),
        ],
        style={
            "display": "flex",
            "flexWrap": "wrap",
            "justifyContent": "center",
            "marginBottom": "30px",
        },
    )


def generate_main_overview_charts(df):
    """Generate the main overview charts with improved genre visualization"""
    # Create a subplot with 2x2 layout but replace pie chart with horizontal bar chart
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Genre Distribution",
            "Songs by Decade",
            "Average Audio Features",
            "Popularity Distribution",
        ),
        specs=[
            [{"type": "bar"}, {"type": "bar"}],
            [{"type": "bar"}, {"type": "histogram"}],
        ],
        horizontal_spacing=0.1,
        vertical_spacing=0.15,
    )

    # 1. Genre Distribution (Horizontal Bar Chart - IMPROVED!)
    genre_counts = df["playlist_genre"].value_counts()
    genre_percentages = (genre_counts / len(df) * 100).round(1)
    colors_bar = ["#ff7f0e", "#d62728", "#2ca02c", "#9467bd", "#8c564b", "#e377c2"]

    fig.add_trace(
        go.Bar(
            x=genre_percentages.values,
            y=genre_percentages.index,
            orientation="h",
            marker_color=colors_bar[: len(genre_percentages)],
            text=[f"{val}%" for val in genre_percentages.values],
            textposition="inside",
            textfont=dict(color="white", size=10, family="Arial Black"),
            hovertemplate="<b>%{y}</b><br>Count: %{customdata:,}<br>Percentage: %{x}%<extra></extra>",
            customdata=genre_counts.values,
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    # 2. Songs by Decade (Vertical Bar Chart)
    df["decade"] = (df["year"] // 10) * 10
    decade_counts = df["decade"].value_counts().sort_index()
    decade_labels = [f"{int(d)}s" for d in decade_counts.index]

    fig.add_trace(
        go.Bar(
            x=decade_labels,
            y=decade_counts.values,
            marker_color="#2E86AB",
            hovertemplate="<b>%{x}</b><br>Songs: %{y:,}<extra></extra>",
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    # 3. Average Audio Features (Vertical Bar Chart)
    audio_features = [
        "danceability",
        "energy",
        "valence",
        "acousticness",
        "speechiness",
        "instrumentalness",
    ]
    feature_averages = df[audio_features].mean()

    fig.add_trace(
        go.Bar(
            x=feature_averages.index,
            y=feature_averages.values,
            marker_color="#F18F01",
            hovertemplate="<b>%{x}</b><br>Average: %{y:.3f}<extra></extra>",
            showlegend=False,
        ),
        row=2,
        col=1,
    )

    # 4. Popularity Distribution (Histogram)
    fig.add_trace(
        go.Histogram(
            x=df["track_popularity"],
            nbinsx=20,
            marker_color="#A23B72",
            hovertemplate="Popularity: %{x}<br>Count: %{y}<extra></extra>",
            showlegend=False,
        ),
        row=2,
        col=2,
    )

    # Update layout
    fig.update_layout(
        height=700,
        showlegend=False,
        title_text="Spotify Dataset Overview",
        title_x=0.5,
        title_font_size=20,
    )

    # Update axes for better readability
    # Genre chart - make y-axis more readable
    fig.update_yaxes(automargin=True, row=1, col=1)
    fig.update_xaxes(title_text="Percentage (%)", row=1, col=1)

    # Audio features chart - rotate labels
    fig.update_xaxes(tickangle=45, row=2, col=1)

    # Decade chart
    fig.update_xaxes(title_text="Decade", row=1, col=2)
    fig.update_yaxes(title_text="Number of Songs", row=1, col=2)

    # Popularity chart
    fig.update_xaxes(title_text="Popularity Score", row=2, col=2)
    fig.update_yaxes(title_text="Count", row=2, col=2)

    # Audio features chart
    fig.update_yaxes(title_text="Average Score", row=2, col=1)

    return fig


def generate_timeline_overview(df):
    """Generate a timeline showing data coverage and key metrics over time"""
    # Group by year and calculate metrics
    yearly_stats = (
        df.groupby("year")
        .agg(
            {
                "track_id": "count",
                "track_popularity": "mean",
                "playlist_genre": lambda x: x.nunique(),
            }
        )
        .reset_index()
    )

    yearly_stats.columns = ["year", "song_count", "avg_popularity", "genre_diversity"]

    # Create timeline chart
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        subplot_titles=(
            "Songs Released per Year",
            "Average Popularity",
            "Genre Diversity",
        ),
        vertical_spacing=0.08,
    )

    # Songs per year
    fig.add_trace(
        go.Scatter(
            x=yearly_stats["year"],
            y=yearly_stats["song_count"],
            mode="lines+markers",
            name="Songs",
            line=dict(color="#2E86AB", width=2),
            fill="tozeroy",
            fillcolor="rgba(46, 134, 171, 0.3)",
            hovertemplate="<b>Year: %{x}</b><br>Songs: %{y:,}<extra></extra>",
        ),
        row=1,
        col=1,
    )

    # Average popularity
    fig.add_trace(
        go.Scatter(
            x=yearly_stats["year"],
            y=yearly_stats["avg_popularity"],
            mode="lines+markers",
            name="Avg Popularity",
            line=dict(color="#A23B72", width=2),
            hovertemplate="<b>Year: %{x}</b><br>Avg Popularity: %{y:.1f}<extra></extra>",
        ),
        row=2,
        col=1,
    )

    # Genre diversity
    fig.add_trace(
        go.Scatter(
            x=yearly_stats["year"],
            y=yearly_stats["genre_diversity"],
            mode="lines+markers",
            name="Genre Diversity",
            line=dict(color="#F18F01", width=2),
            fill="tozeroy",
            fillcolor="rgba(241, 143, 1, 0.3)",
            hovertemplate="<b>Year: %{x}</b><br>Genres: %{y}<extra></extra>",
        ),
        row=3,
        col=1,
    )

    fig.update_layout(
        height=500,
        showlegend=False,
        title_text="Dataset Timeline Overview",
        title_x=0.5,
    )

    # Update axes labels
    fig.update_xaxes(title_text="Year", row=3, col=1)
    fig.update_yaxes(title_text="Number of Songs", row=1, col=1)
    fig.update_yaxes(title_text="Popularity Score", row=2, col=1)
    fig.update_yaxes(title_text="Number of Genres", row=3, col=1)

    return fig


def get_main_visualization_content():
    """Main function to return the main visualization content"""
    df = load_main_data()
    kpis = calculate_kpis(df)

    return html.Div(
        [
            # Header section
            html.Div(
                [
                    html.H3(
                        "Dataset Overview",
                        style={
                            "textAlign": "center",
                            "marginBottom": "30px",
                            "color": "#2E86AB",
                        },
                    ),
                    html.P(
                        [
                            "This dashboard analyzes approximately 30,000 songs from Spotify, spanning multiple decades and genres. "
                            "The data includes audio features, popularity metrics, and temporal information to provide comprehensive "
                            "insights into music trends and characteristics."
                        ],
                        style={
                            "textAlign": "center",
                            "maxWidth": "800px",
                            "margin": "0 auto",
                            "color": "#666",
                        },
                    ),
                ],
                style={"marginBottom": "30px"},
            ),
            create_kpi_cards(kpis),
            html.Div(
                [
                    html.H4(
                        "Key Metrics Overview",
                        style={"textAlign": "center", "marginBottom": "20px"},
                    ),
                    dcc.Graph(
                        id="main-overview-charts",
                        figure=generate_main_overview_charts(df),
                        config={"responsive": True, "displayModeBar": False},
                    ),
                ],
                style={"marginBottom": "30px"},
            ),
            html.Div(
                [
                    html.H4(
                        "Dataset Timeline",
                        style={"textAlign": "center", "marginBottom": "20px"},
                    ),
                    dcc.Graph(
                        id="timeline-overview",
                        figure=generate_timeline_overview(df),
                        config={"responsive": True, "displayModeBar": False},
                    ),
                ],
                style={"marginBottom": "30px"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H5("📊 Data Coverage", style={"color": "#2E86AB"}),
                            html.P(
                                [
                                    f"Our dataset spans {kpis['year_range']} with {kpis['total_songs']:,} tracks from "
                                    f"{kpis['total_artists']:,} unique artists across {kpis['total_genres']} main genres and "
                                    f"{kpis['total_subgenres']} subgenres."
                                ]
                            ),
                        ],
                        style={
                            "width": "48%",
                            "display": "inline-block",
                            "verticalAlign": "top",
                        },
                    ),
                    html.Div(
                        [
                            html.H5("🎯 Analysis Focus", style={"color": "#A23B72"}),
                            html.P(
                                [
                                    "The analysis focuses on identifying trends in genre popularity, audio characteristics, "
                                    "and temporal patterns to help music industry professionals make informed decisions."
                                ]
                            ),
                        ],
                        style={
                            "width": "48%",
                            "display": "inline-block",
                            "marginLeft": "4%",
                            "verticalAlign": "top",
                        },
                    ),
                ],
                style={
                    "backgroundColor": "#f8f9fa",
                    "padding": "20px",
                    "borderRadius": "8px",
                    "marginTop": "20px",
                },
            ),
        ]
    )
