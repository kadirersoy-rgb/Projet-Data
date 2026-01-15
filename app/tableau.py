from dash import Dash, html, dcc, Input, Output
import requests
import pandas as pd
import plotly.graph_objects as go
from common import use_data

def creation_app_dash(srv_Flask):
    """ Création de l'application Dash pour la comparaison des Régions """
    
    app_Dash = Dash(__name__, server=srv_Flask, routes_pathname_prefix="/map/", suppress_callback_exceptions=True)

    # --- Chargement des données ---
    df_all = use_data.charger_les_data(["2018", "2019", "2020", "2021"])
    df_all["ANNEE"] = df_all["ANMOIS"].astype(str).str[:4]
    
    annees_disponibles = sorted(df_all["ANNEE"].unique())

    # --- Composants HTML ---
    header = html.Div(className = 'header', 
        children = [
            html.Img(src='/static/images/ESIEE_Paris_logo.png', className='logo', alt='ESIEE Paris Logo'),
            html.H1("Comparaison des Régions", className = "titre_header_diagramme")
        ])

    Dropdown_annees = html.Div(className="dropdown_annees",
        children = [
            html.Label("Sélectionner une année:"),
            dcc.Dropdown(
                id="annee_dropdown_map",
                options=[{"label":str(annee), "value": annee} for annee in annees_disponibles],
                value=annees_disponibles[0]
            )
        ]) 

    Graph_map = dcc.Graph(id="graphe_scatter_regions", className="graphe", style={"height": "80vh", "width": "100%"})

    # --- Layout ---
    # MODIFICATION 1 : On retire le style backgroundColor du Div principal
    app_Dash.layout =  html.Div([
        html.Link(rel="stylesheet", href="/static/css/diagramme.css"),
        header,
        Dropdown_annees,
        Graph_map
    ])

    # --- Callback ---
    @app_Dash.callback(
        Output("graphe_scatter_regions", "figure"),
        Input("annee_dropdown_map", "value")
    )
    def update_map(annee):
        
        url = f"http://127.0.0.1:5000/api/data?year={annee}" 
        
        try:
            resp = requests.get(url)
            data_json = resp.json()
            df = pd.DataFrame(data_json)
        except:
            return go.Figure()

        if df.empty:
             return go.Figure().update_layout(
                 title="Pas de données", 
                 template="plotly_dark",
                 paper_bgcolor='black', # Fond noir même si vide
                 plot_bgcolor='black'
             )

        # Groupement par RÉGION
        region_stats = df.groupby('REGION').agg({
            'APT_PAX_dep': 'mean',
            'APT_PAX_arr': 'mean'
        }).reset_index()

        region_stats.columns = ['REGION', 'avg_dep', 'avg_arr']

        # Création du Scatter Plot
        trace = go.Scatter(
            x=region_stats['avg_arr'], 
            y=region_stats['avg_dep'], 
            mode='markers',
            text=region_stats['REGION'],
            # textposition="top center",
            name='Régions',
            hovertemplate="<b>%{text}</b><br>Arrivée (moy): %{x:.0f}<br>Départ (moy): %{y:.0f}<extra></extra>",
            marker=dict(
                color='#1f77b4', 
                size=8,
                line=dict(width=1, color='White')
            ),
            # Texte en blanc pour être lisible sur le fond noir
            textfont=dict(
                color='white' 
            )
        )

        layout = go.Layout(
            title=f"Moyenne des passagers par Région en {annee}",
            xaxis=dict(
                title="Passagers à l'arrivée (Moyenne)", 
                type='log', 
                gridcolor='#444' # Grille gris foncé
            ),
            yaxis=dict(
                title='Passagers au départ (Moyenne)', 
                type='log', 
                gridcolor='#444'
            ),
            hovermode="closest",
            template="plotly_dark", # Gère les axes et le texte en blanc automatiquement
            
            # MODIFICATION 2 : On force le fond du graphique en noir
            paper_bgcolor='black', # La zone autour du graphique (titre, légendes)
            plot_bgcolor='black'   # La zone de dessin (grille)
        )

        fig = go.Figure(data=[trace], layout=layout)

        return fig