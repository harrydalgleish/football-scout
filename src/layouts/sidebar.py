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
            id="season",
            options=[]
        ),
        html.Label("Team"),
        dcc.Dropdown(
            id="team",
            options=[]
        ),
        html.Label("Opposition"),
        dcc.Dropdown(
            id="opposition",
            options=[]
        ),
        html.Label("Home/Away"),
        dcc.Dropdown(
            id="HomeAway",
            options=[]
        )

    ],

    style = {
        "width":"300px",
        "padding":"20px",
        "backgroundColor":"#0B1F00"
    }

)