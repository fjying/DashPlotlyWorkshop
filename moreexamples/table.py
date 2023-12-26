from dash import Dash, html
import pandas as pd
import os

workshop_folder_path = '/Users/jf3375/PycharmProjects/Dash_Plotly_Workshop'
os.chdir(os.path.join(workshop_folder_path, 'data'))
df =pd.read_csv('gapminderDataFiveYear.csv')

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


app = Dash(__name__)

app.layout = html.Div([
    html.H4(children='GapMinderData'),
    generate_table(df, max_rows = df.shape[0])
])

if __name__ == '__main__':
    app.run(port=8052, debug = False)