import pandas as pd
import plotly.graph_objs as go

import dash_html_components as html
import dash_core_components as dcc

def get_speechiness_line_chart_content(df):
    fig = generate_speechiness_line_chart(df)
    return html.Div([
        dcc.Graph(figure=fig)
    ])

def generate_speechiness_line_chart(df):
    """
    Generates a Plotly line chart showing the median and average speechiness of popular songs on Spotify over the years.
    """
    df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'], errors='coerce')
    df['year'] = df['track_album_release_date'].dt.year

    df_filtered = df[df['track_popularity'] > 60].copy()
    agg = df_filtered.groupby('year')['speechiness'].agg(['mean', 'median']).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=agg['year'], y=agg['median'],
        mode='lines+markers',
        name='Median Speechiness',
        line=dict(color='#2ca02c', width=2.5)
    ))
    fig.add_trace(go.Scatter(
        x=agg['year'], y=agg['mean'],
        mode='lines+markers',
        name='Mean Speechiness',
        line=dict(color='#1f77b4', width=2.5)
    ))
    fig.update_layout(
        title="Median and Average Speechiness of Popular Songs on Spotify Over the Years",
        xaxis_title="Year",
        yaxis_title="Speechiness",
        template="simple_white",
        legend=dict(x=0.01, y=0.99)
    )
    return fig

