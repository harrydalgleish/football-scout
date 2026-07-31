from dash import html


def pitch_panel():

    return html.Div(

        [

            html.H3(
                "Formation",
                style={
                    "color": "white",
                    "margin": "10px"
                }
            ),

            html.Div(

                id="pitch",

                style={
                    "flex": 1,
                    "margin": "10px",
                    "border": "2px solid #2c2c2c",
                    "borderRadius": "10px",
                    "backgroundColor": "#0d2b18"
                }

            )

        ],

        style={
            "display": "flex",
            "flexDirection": "column",
            "height": "50%",
            "backgroundColor": "#09122A"
        }

    )