from dash import Dash, html

from layouts.sidebar import sidebar
from layouts.analysis import analysis_panel
from layouts.pitch import pitch_panel

app = Dash(__name__)

app.title = "Football Scout"

app.layout = html.Div(

    [

        sidebar(),

        html.Div(

            [

                analysis_panel(),

                pitch_panel()

            ],

            id="main",

            style={
                "display": "flex",
                "flexDirection": "column",
                "flex": 1,
                "height": "100vh"
            }

        )

    ],

    style={
        "display": "flex",
        "height": "100vh",
        "backgroundColor": "#04001F"
    }

)

if __name__ == "__main__":
    app.run(debug=True)