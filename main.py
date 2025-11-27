# V0 Start of collaboration : ERSOY-POKRYWA ESIEE Paris E3 FIdir
from dash import Dash, html, dcc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
app = Dash(__name__)

app.layout = [
    html.Div(children='My First App with Data and a Graph'),
    dag.AgGrid(
        rowData=df.to_dict('records'),
        columnDefs=[{"field": i} for i in df.columns]
    ),
    dcc.Graph(figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg'))
]

if __name__ == "__main__":
    app.run() 