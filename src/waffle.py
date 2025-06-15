import plotly.graph_objects as go

def generate_waffle_figure(counts, title):
    total_squares = 100
    n_rows = 10
    n_cols = 10

    color_map = {
        "Low (0.0–0.2)": "#A6CEE3",
        "Medium (0.2–0.5)": "#1F78B4",
        "High (0.5–1.0)": "#33A02C"
    }

    # Préparer les blocs
    category_blocks = []
    hover_texts = []
    for category, value in counts.items():
        proportion = int(round(value / sum(counts.values()) * total_squares))
        category_blocks.extend([category] * proportion)
        hover_texts.extend([f"{category}<br>{(value / sum(counts.values()) * 100):.1f}%"] * proportion)

    while len(category_blocks) < total_squares:
        category_blocks.append("")
        hover_texts.append("")

    x_vals, y_vals, colors = [], [], []

    for i in range(total_squares):
        row = i // n_cols
        col = i % n_cols
        category = category_blocks[i]
        color = color_map.get(category, "#FFFFFF")

        x_vals.append(col)
        y_vals.append(n_rows - 1 - row)
        colors.append(color)

    fig = go.Figure(
        data=go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="markers",
            marker=dict(
                size=38,
                color=colors,
                symbol='square',
                line=dict(color='#DDDDDD', width=1)
            ),
            text=hover_texts,
            hoverinfo="text"
        )
    )

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, family='Arial Black')),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=20, r=20, t=50, b=20),
        height=420,
        plot_bgcolor='white',
        showlegend=False
    )

    return fig
