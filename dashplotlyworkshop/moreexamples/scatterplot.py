from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import os


data_folder_path = os.path.join(os.path.dirname(os.getcwd()), 'data')
df =pd.read_csv(os.path.join(data_folder_path, 'gapminderDataFiveYear.csv'))

app = Dash(external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div([
    html.H4(
        children='Relationships between the GDP per Capita Growth, Population, Country Continent and Life Expectancy across Time'),
    html.Wbr(),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
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
    app.run(host = '127.0.0.1', port=8053, debug = True)