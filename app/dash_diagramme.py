from dash import Dash, html, dcc, Input, Output
import requests
import plotly.express as px
import pandas as pd


def creation_app_dash(srv_Flask):
    app_Dash = Dash(__name__, server=srv_Flask, routes_pathname_prefix="/diagramme/", suppress_callback_exceptions=True)

    header = html.Div(className = 'header', 
    children = [
    html.Img(src='/static/images/ESIEE_Paris_logo.png', className='logo', alt='ESIEE Paris Logo'),
    html.H1("Diagramme", className = "titre_header_accueil")
    ])

    app_Dash.layout =  html.Div([
    html.Link(rel="stylesheet", href="/static/css/index.css"),
    header
    ])

    #### Test API pour un filtrage dynamique ####

    # ,
    # dcc.Dropdown(
    #     id="annee-selectionnee",
    #     options=[
    #         {"label": "2018", "value": "2018"},
    #         {"label": "2019", "value": "2019"},
    #         {"label": "2020", "value": "2020"},
    #         {"label": "2021", "value": "2021"},],
    #     value="2018",
    # ),
    # dcc.Graph(id="graph")
    

    # @app_Dash.callback(
    #     Output("graph", "figure"),
    #     Input("annee-selectionnee", "value"),
    # )

    # def update_graph(annee_selectionnee):
    #     resp = requests.get(f"http://127.0.0.1:5000/api/data?year={annee_selectionnee}")

    #     data = resp.json()  
    #     df = pd.DataFrame(data)
    #     fig = px.bar(df, x="year", y="value", title=f"Valeurs pour {annee_selectionnee}")
    #     return fig




    

    