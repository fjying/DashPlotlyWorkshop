import os
import plotly.express as px
import pandas as pd
from datetime import timedelta, datetime
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from dashplotlyworkshop.styles.styles import colors, TITLE_STYLE, DROPDOWN_STYLE

# Change directory to local workshop folder path
data_folder_path = os.path.join(os.path.dirname(os.getcwd()), 'data')


# Import and Process Data
def process_date_column(df, date_column='index'):
    df[date_column] = df[date_column].apply(
        lambda x: datetime.strptime(x[:13], "%Y-%m-%d %H"))
    df = df.rename(columns={'index': 'time'})
    return df

type_allocs_rts = process_date_column(pd.read_csv(os.path.join(data_folder_path, 'daily_type-allocs_rts_type_allocs.csv')))
date_values_rts = pd.date_range(start='2020-01-01', end='2020-12-29')
date_values_rts = [str(i)[:10] for i in date_values_rts]

# Build Dashboard
# See the looks of themes: https://bootswatch.com/spacelab/
app = Dash(external_stylesheets=[dbc.themes.SPACELAB])
app.title = 'singlepagedashboard'

app.layout = html.Div(children=[

    dbc.Row(
        dbc.Col(html.H1(children='Reliability Cost Index Visualization',
                        style=TITLE_STYLE))
    ),

    dbc.Row(
        dbc.Col([
            html.Label('Select Day'),
            dcc.Dropdown(date_values_rts,
                         id='date_values_rts',
                         value=date_values_rts[1],
                         style=DROPDOWN_STYLE)
        ])
    ),

    html.Wbr(),

    dbc.Row(
        dbc.Col(html.H3('Plot of the Day Selected'))
    ),

    dbc.Row(
        dcc.Graph(id='fig_type_allocs_day')
    )

], style= {"margin-left": "2rem",
    "margin-right": "2rem",
    "margin-top": "2rem"})


@app.callback(
    Output('fig_type_allocs_day', 'figure'),
    Input('date_values_rts', 'value')
)
def plot_fig_type_allocs_of_day(day):
    input_start_date = datetime(int(day[0:4]), int(day[5:7]), int(day[8:10]))  # By default 0 hour 0 minutes
    input_start_date_verbal = input_start_date.strftime("%b %d, %Y")

    # Create 24 hours interval on the input_date
    daterange_rts = pd.date_range(input_start_date, input_start_date + timedelta(hours=23), freq='H')

    fig_type_allocs_day = px.line(type_allocs_rts[type_allocs_rts['time'].isin(daterange_rts)],
                                  x='time', y=['RTPV', 'WIND', 'PV'],
                                  hover_data={"time": "|Hour %H, %b %d"})

    fig_type_allocs_day.update_layout(
        title='Hourly Time Series of Asset Type Reliability Cost Index on {}'.format(input_start_date_verbal),
        xaxis_title='Time',
        yaxis_title='Reliability Cost Index ($)',
        legend_title='Asset Type',
        font_family='sans-serif', font_color=colors['text_1'],
        title_font_color=colors['plottitle'],
        legend=dict(x=1, y=1), legend_font_size=20, title_font_size=25,
        font_size=16,
        plot_bgcolor=colors['lightbackground'],
        paper_bgcolor=colors['background'])

    return fig_type_allocs_day


if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1', port=8060)