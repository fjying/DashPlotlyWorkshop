import dash_bootstrap_components as dbc

from dash import dcc, html, Input, Output

from dashplotlyworkshop.multiplepagesdashboard.app_define import app
from dashplotlyworkshop.styles.styles import CONTENT_STYLE, SIDEBAR_STYLE
from pages.homepage import html_div_home_page
from pages.riskallocation import html_div_risk_allocation

sidebar = html.Div(
    [
        html.H2("DASH"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"), # There would be the blue highlight bar when the link is active
                dbc.NavLink("Risk Allocation", href="/riskallocation", active="exact")
            ],
            vertical=True,
            pills=True, # Allow the active higlight bar
        ),
    ],
    style=SIDEBAR_STYLE
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/":
        return html_div_home_page
    elif pathname == "/riskallocation":
        return html_div_risk_allocation
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(port=8051, debug=True)


