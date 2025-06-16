import pandas as pd
import plotly.express as px
import numpy as np  # Import numpy for random number generation

# === Données ===
df = pd.read_csv("./assets/data/spotify_songs.csv")


# Convert release date column to datetime objects, handling potential errors
df["track_album_release_date"] = pd.to_datetime(
    df["track_album_release_date"], errors="coerce"
)

# Drop rows where date conversion resulted in NaT (Not a Time)
df.dropna(subset=["track_album_release_date"], inplace=True)

# --- Season Categorization ---

# Extract the month from the release date
df["release_month"] = df["track_album_release_date"].dt.month


# Define a function to map month to season
def get_season(month):
    """Maps a month number to a season."""
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:  # months 9, 10, 11
        return "Fall"


# Apply the function to create the 'season' column
df["season"] = df["release_month"].apply(get_season)

# --- Jitter Application ---
# To better visualize density when points are quantized (e.g., integers),
# we add a small amount of random horizontal noise (jitter) to the popularity score.

# Define the possible jitter values: [-0.5, -0.4, -0.3, ..., 0.3, 0.4, 0.5]
# We use np.round to handle potential floating point inaccuracies with np.arange.
possible_jitters = np.round(np.arange(-0.5, 0.6, 0.2), 1)

# Randomly choose a jitter value from the possible options for each song.
random_jitters = np.random.choice(possible_jitters, size=len(df))

# Apply the discrete jitter to the popularity score.
df["popularity_jittered"] = df["track_popularity"] + random_jitters

# --- Visualization ---

# Create the beeswarm plot (using px.strip)
fig = px.strip(
    df,
    x="popularity_jittered",
    y="season",
    color="playlist_genre",  # Color points by season for better distinction
    stripmode="overlay",  # 'group' is another option
    title="Song Popularity by Release Season (Beeswarm Plot)",
    labels={"track_popularity": "Popularity Score", "season": "Season"},
    category_orders={
        "season": ["Winter", "Spring", "Summer", "Fall"]
    },  # Ensure consistent order
)

# --- Layout and Styling ---

# Update layout for a cleaner look
fig.update_layout(
    plot_bgcolor="white",  # Set background to white
    xaxis=dict(
        title="Track Popularity",
        showgrid=True,
        gridcolor="LightGray",
        zeroline=True,
        zerolinecolor="Gainsboro",
    ),
    yaxis=dict(
        title="Release Season",
        showgrid=True,
        gridcolor="LightGray",
        zeroline=True,
        zerolinecolor="Gainsboro",
    ),
    legend_title_text="Genre",
    boxgap=0,
    height=1000,  # Adjust height for better viewing
)

# Enhance the 'beeswarm' appearance by adjusting jitter
# A jitter of 1 distributes points across the full width of the category
# THE MOST CRITICAL PART FOR THE DESIRED VISUAL EFFECT
fig.update_traces(
    jitter=1,  # Maximize horizontal spread within the strip
    marker=dict(
        size=3,  # EXTREMELY SMALL POINTS: Essential for visualizing fine density
    ),
)

# --- Adding Statistical Overlays (Box Plots/Violin Plots) ---
# This is a significant improvement to show central tendency and spread.
# We will add a box plot or violin plot on top of the beeswarm.
# Violin plots are often preferred as they show density.

# Option 1: Add Violin Plots
fig.add_trace(
    px.violin(
        df,
        x="track_popularity",
        y="season",
        color="season",
        box=True,  # Show a box plot inside the violin
        points=False,  # Do not show individual points in the violin plot (already in strip plot)
        orientation="h",  # Horizontal orientation
        category_orders={"season": ["Winter", "Spring", "Summer", "Fall"]},
    )
    .update_traces(
        # Make the violin plots transparent or less prominent to let the beeswarm show through
        fillcolor="rgba(0,0,0,0)",  # Transparent fill
        line_color="black",  # Black outline
        line_width=1,
        marker_color="black",  # For the box plot part
        opacity=0.7,  # Slight opacity if using fill color
    )
    .data[0]  # Get the first trace from the violin plot
)

# Adjust layout to accommodate the new traces
fig.update_layout(showlegend=False)  # Hide the duplicate legend from the violin plot

# Reorder traces to ensure beeswarm is on top if desired (optional, depends on visual preference)
# fig.data = fig.data[::-1] # Reverse order to put strip plot on top

# --- Display and Save ---

# To display the figure in a script or notebook
fig.show()

# To save the figure to an HTML file
# fig.write_html('spotify_popularity_beeswarm.html')
