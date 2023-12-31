import os
import plotly.express as px
import pandas as pd
from datetime import timedelta, datetime
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from dashplotlyworkshop.styles.styles import colors, TITLE_STYLE, DROPDOWN_STYLE, CONTENT_STYLE
from dashplotlyworkshop.multiplepagesdashboard.app_define import app

# Change directory to workshop folder path
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

# Exactly same as single page dashboard, except for we pass it to variable instead of directly to app.layout
html_div_risk_allocation = html.Div(children=[

    dbc.Row(
        dbc.Col(html.H3(children='Reliability Cost Index Visualization',
                        style=TITLE_STYLE))
        , justify='start', align='start'),

    dbc.Row(
        dbc.Col([
            html.Label('Select Day'),
            dcc.Dropdown(date_values_rts,
                         id='date_values_rts',
                         value=date_values_rts[0],
                         style=DROPDOWN_STYLE)
        ])
    ),

    html.Wbr(),

    html.H5(children = ['Plot of the Day Selected:  ',
                       html.Div(
                           id='date_verbal',
                           style={'display': 'inline'})],
            style = {'font-size': 20, 'font-weight': 'bold', 'color': 'black',
                  'padding-left': '0px'}
           ),

    dbc.Row([dbc.Col([
        dcc.Graph(
            id='fig_type_allocs_day'
        )
    ])
    ], justify = 'center', align='center')

])


@app.callback(
    Output('fig_type_allocs_day', 'figure'),
    Output('date_verbal', 'children'),
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
        # title='Hourly Time Series of {} Asset Type Reliability Cost Index, updated on {}'.format(version, todaydate_verbal),
        xaxis_title='Date',
        yaxis_title='Reliability Cost Index ($)',
        legend_title='Asset Type',
        font_family='sans-serif', font_color=colors['text_1'],
        title_font_color=colors['plottitle'],
        legend=dict(x=1, y=1), legend_font_size=20, title_font_size=25,
        font_size=16,
        plot_bgcolor=colors['lightbackground'],
        paper_bgcolor=colors['background'])

    return fig_type_allocs_day, input_start_date_verbal