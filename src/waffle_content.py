import dash_html_components as html
import dash_core_components as dcc
from waffle import generate_waffle_figure
from preprocess import load_and_clean_data


def classify_speechiness(val):
    if val < 0.2:
        return "Low (0.0–0.2)"
    elif val < 0.5:
        return "Medium (0.2–0.5)"
    else:
        return "High (0.5–1.0)"


def get_waffle_content():
    df = load_and_clean_data()

    df["speechiness_level"] = df["speechiness"].apply(classify_speechiness)

    popular_counts = (
        df[df["track_popularity"] > 60]["speechiness_level"].value_counts().to_dict()
    )
    less_popular_counts = (
        df[df["track_popularity"] <= 60]["speechiness_level"].value_counts().to_dict()
    )

    fig_popular = generate_waffle_figure(popular_counts, "Popular Songs")
    fig_less = generate_waffle_figure(less_popular_counts, "Less Popular Songs")

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [dcc.Graph(figure=fig_popular)],
                        style={"width": "48%", "display": "inline-block"},
                    ),
                    html.Div(
                        [dcc.Graph(figure=fig_less)],
                        style={
                            "width": "48%",
                            "display": "inline-block",
                            "marginLeft": "4%",
                        },
                    ),
                ],
                style={"marginTop": "30px"},
            )
        ]
    )
