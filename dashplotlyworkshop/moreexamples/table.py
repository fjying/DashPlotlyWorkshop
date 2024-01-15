from dash import Dash, html
import pandas as pd
import os

data_folder_path = os.path.join(os.path.dirname(os.getcwd()), 'data')
df =pd.read_csv(os.path.join(data_folder_path, 'gapminderDataFiveYear.csv'))

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
    html.H3(children='Visualize Panel Data of GapMinderData'),
    generate_table(df, max_rows = df.shape[0])
])

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port=8052, debug = False)