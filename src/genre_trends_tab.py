import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def load_data():
    """Load and preprocess data for genre trends analysis"""
    df = pd.read_csv("./assets/data/spotify_songs.csv")
    df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'], errors='coerce')
    df['year'] = df['track_album_release_date'].dt.year
    
    df = df.dropna(subset=['year', 'track_popularity', 'playlist_genre', 'playlist_subgenre'])
    df = df[df['year'] >= 2000]
    
    return df

def generate_genre_evolution_chart(df):
    """Generate line chart showing genre popularity evolution over time"""
    genre_evolution = df.groupby(['year', 'playlist_genre'])['track_popularity'].mean().reset_index()
    
    fig = go.Figure()
    
    # Define colors for each genre
    colors = {
        'pop': '#ff7f0e',
        'rock': '#d62728', 
        'rap': '#2ca02c',
        'edm': '#9467bd',
        'r&b': '#8c564b',
        'latin': '#e377c2'
    }
    
    for genre in genre_evolution['playlist_genre'].unique():
        genre_data = genre_evolution[genre_evolution['playlist_genre'] == genre]
        
        fig.add_trace(go.Scatter(
            x=genre_data['year'],
            y=genre_data['track_popularity'],
            mode='lines+markers',
            name=genre.upper(),
            line=dict(color=colors.get(genre, '#1f77b4'), width=3),
            marker=dict(size=6),
            hovertemplate=f'<b>{genre.upper()}</b><br>' +
                         'Year: %{x}<br>' +
                         'Avg Popularity: %{y:.1f}<extra></extra>'
        ))
    
    fig.update_layout(
        title="Genre Popularity Evolution (2000-2020)",
        xaxis_title="Year",
        yaxis_title="Average Popularity Score",
        template="plotly_white",
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def generate_subgenre_heatmap(df):
    """Generate heatmap showing subgenre performance across time periods"""
    # time periods
    df['period'] = pd.cut(df['year'], 
                         bins=[1999, 2004, 2008, 2012, 2016, 2021],
                         labels=['2000-2004', '2005-2008', '2009-2012', '2013-2016', '2017-2020'])
    
    # Average popularity by subgenre and period
    subgenre_heatmap_data = df.groupby(['playlist_subgenre', 'period'])['track_popularity'].mean().reset_index()
    
    # Pivot for heatmap
    heatmap_pivot = subgenre_heatmap_data.pivot(index='playlist_subgenre', 
                                               columns='period', 
                                               values='track_popularity')
    
    # Fill NaN values with 0
    heatmap_pivot = heatmap_pivot.fillna(0)
    heatmap_pivot['avg'] = heatmap_pivot.mean(axis=1)
    # sort by overall average
    heatmap_pivot = heatmap_pivot.sort_values('avg', ascending=False).drop('avg', axis=1)
    
    # Take top 15 subgenres to avoid overcrowding
    heatmap_pivot = heatmap_pivot.head(15)
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        colorscale='RdYlBu_r',
        zmid=50, 
        colorbar=dict(title="Avg Popularity"),
        hovertemplate='Period: %{x}<br>' +
                     'Subgenre: %{y}<br>' +
                     'Avg Popularity: %{z:.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Top 15 Subgenres Performance Across Time Periods",
        xaxis_title="Time Period",
        yaxis_title="Subgenre",
        height=600,
        template="plotly_white"
    )
    
    return fig

def generate_audio_features_radar(df, selected_genre='pop'):
    """Generate radar chart showing audio features for selected genre"""
    # Audio features
    features = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'speechiness']
    
    # Average features for the selected genre
    genre_features = df[df['playlist_genre'] == selected_genre][features].mean()
    
    # Overall average for comparison
    overall_features = df[features].mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=genre_features.values,
        theta=features,
        fill='toself',
        name=f'{selected_genre.upper()} Average',
        line_color='#ff7f0e'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=overall_features.values,
        theta=features,
        fill='toself',
        name='Overall Average',
        line_color='#1f77b4',
        opacity=0.6
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title=f"Audio Features Profile: {selected_genre.upper()} vs Overall Average",
        height=500
    )
    
    return fig

def generate_growth_analysis(df):
    """Analyze genre growth rates over time"""
    # Popularity by genre for first and last 3 years
    early_period = df[df['year'].between(2000, 2002)].groupby('playlist_genre')['track_popularity'].mean()
    late_period = df[df['year'].between(2018, 2020)].groupby('playlist_genre')['track_popularity'].mean()
    
    growth_df = pd.DataFrame({
        'Early Period (2000-2002)': early_period,
        'Late Period (2018-2020)': late_period
    }).fillna(0)
    
    growth_df['Growth'] = growth_df['Late Period (2018-2020)'] - growth_df['Early Period (2000-2002)']
    growth_df['Growth %'] = (growth_df['Growth'] / growth_df['Early Period (2000-2002)']) * 100
    growth_df = growth_df.sort_values('Growth', ascending=True)
    
    fig = go.Figure()
    
    # Color bars based on positive/negative growth
    colors = ['#d62728' if x < 0 else '#2ca02c' for x in growth_df['Growth']]
    
    fig.add_trace(go.Bar(
        x=growth_df['Growth'],
        y=growth_df.index,
        orientation='h',
        marker_color=colors,
        hovertemplate='<b>%{y}</b><br>' +
                     'Growth: %{x:.1f} points<br>' +
                     '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Genre Popularity Growth: 2018-2020 vs 2000-2002",
        xaxis_title="Popularity Change (points)",
        yaxis_title="Genre",
        template="plotly_white",
        height=400
    )
    
    return fig

def get_genre_trends_content():
    """Main function to return the content for Genre Trends tab"""
    df = load_data()
    
    return html.Div([
        # Description section
        html.Div([
            html.H3("Genre Trends and Market Evolution"),
            html.P([
                "This section presents a detailed analysis of musical genre evolution and their popularity over time. "
                "It allows identification of growing genres, declining ones, and specific characteristics that define "
                "success within each genre. This analysis directly supports strategic decision-making for target genre selection."
            ]),
            html.Ul([
                html.Li("Which genres or subgenres have experienced the highest growth in popularity over the past 20 years?"),
                html.Li("Which genres are declining in popularity?"),
                html.Li("Do certain subgenres consistently outperform others across multiple years?"),
                html.Li("When different genres grow in popularity, can we link it to specific audio variables?")
            ])
        ], style={'marginBottom': '30px'}),
        
        # Genre Evolution Line Chart
        html.Div([
            html.H4("Genre Popularity Evolution Over Time"),
            html.P("Track how the average popularity of major music genres has evolved over the past two decades."),
            dcc.Graph(
                id='genre-evolution-chart',
                figure=generate_genre_evolution_chart(df),
                config={'responsive': True}
            )
        ], style={'marginBottom': '40px'}),
        
        # Growth Analysis
        html.Div([
            html.H4("Genre Growth Analysis"),
            html.P("Compare early period (2000-2002) vs recent period (2018-2020) to identify growth trends."),
            dcc.Graph(
                id='growth-analysis-chart',
                figure=generate_growth_analysis(df),
                config={'responsive': True}
            )
        ], style={'marginBottom': '40px'}),
        
        # Subgenre Heatmap
        html.Div([
            html.H4("Top Subgenres Performance Across Time Periods"),
            html.P("Heatmap showing how the top 15 subgenres performed across different time periods."),
            dcc.Graph(
                id='subgenre-heatmap',
                figure=generate_subgenre_heatmap(df),
                config={'responsive': True}
            )
        ], style={'marginBottom': '40px'}),
        
        # Audio Features Analysis
        html.Div([
            html.H4("Audio Features Profile by Genre"),
            html.P("Compare audio characteristics between genres to understand what drives popularity."),
            html.Div([
                html.Label("Select Genre:"),
                dcc.Dropdown(
                    id='genre-selector',
                    options=[{'label': genre.upper(), 'value': genre} 
                            for genre in sorted(df['playlist_genre'].unique())],
                    value='pop',
                    style={'width': '200px', 'margin': '10px 0'}
                )
            ]),
            dcc.Graph(
                id='audio-features-radar',
                config={'responsive': True}
            )
        ])
    ])

def register_genre_trends_callbacks(app):
    """Register callbacks for interactive components"""
    
    @app.callback(
        Output('audio-features-radar', 'figure'),
        [Input('genre-selector', 'value')]
    )
    def update_radar_chart(selected_genre):
        df = load_data()
        return generate_audio_features_radar(df, selected_genre)