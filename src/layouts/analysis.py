from dash import html

def analysis_panel():

    return html.Div(
        [

            html.Div(

                [

                    html.H2(
                        "Match Analysis",
                        style={
                            "color": "white",
                            "margin": 0
                        }
                    ),

                    html.Button(
                        "📊",
                        id="switch_panel",
                        style={
                            "float": "right"
                        }
                    )

                ],

                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "padding": "10px"
                }

            ),

            html.Div(

                id="analysis_content",

                style={
                    "flex": 1,
                    "margin": "10px",
                    "border": "2px solid #2c2c2c",
                    "borderRadius": "10px",
                    "backgroundColor": "#101820"
                }

            )

        ],

        style={
            "display": "flex",
            "flexDirection": "column",
            "height": "50%"
        }

    )