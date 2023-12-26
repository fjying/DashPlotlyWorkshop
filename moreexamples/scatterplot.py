from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import os


workshop_folder_path = '/Users/jf3375/PycharmProjects/Dash_Plotly_Workshop'
os.chdir(os.path.join(workshop_folder_path, 'data'))
df =pd.read_csv('gapminderDataFiveYear.csv')

app = Dash(external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    )
])


@callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55, template="plotly_dark")

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run(port=8053, debug = False)