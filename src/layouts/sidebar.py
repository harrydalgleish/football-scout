from dash import html, dcc

def sidebar():
    return html.Div([
        html.H2("Football Scout"),
        html.Label("Competition"),
        dcc.Dropdown(
            id="competition",
            options=[]
        ),
        html.Label("Season"),
        dcc.Dropdown(
            id="season"
        ),
        html.Label("Team"),
        dcc.Dropdown(
            id="team"
        ),
        html.Label("Opposition"),
        dcc.Dropdown(
            id="opposition"
        ),
        html.Label("Home/Away"),
        dcc.Dropdown(
            id="HomeAway"
        )

    ])