from dash import html
import dash_bootstrap_components as dbc


html_div_home_page = html.Div(
    children = [
        dbc.Row([
            dbc.Col([html.H2('Multipages Dashboard')]),
        ], justify='start', align = 'center'),

        html.Wbr(),

        dbc.Row([
            dbc.Col(html.P("Sample Home Page"))
        ])
])