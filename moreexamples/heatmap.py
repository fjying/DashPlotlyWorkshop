import plotly.express as px
import xarray as xr
from dash import Dash, html, dcc

# Load xarray from dataset included in the xarray tutorial
airtemps = xr.tutorial.open_dataset('air_temperature').air.sel(lon=250.0)
fig = px.imshow(airtemps.T, color_continuous_scale='RdBu_r', origin='lower')
fig.show()

app = Dash(__name__)

app.layout = html.Div([
    html.H4(children='Heatmap of Temperature Changes across Latitude and Time'),
    html.Br(),
    dcc.Graph(
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(port=8054, debug = False)