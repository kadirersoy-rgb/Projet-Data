'''
Module pour créer une application Dash affichant des diagrammes basés sur les données de passagers
'''

from dash import Dash, html, dcc, Input, Output
import requests
import plotly.express as px
import pandas as pd
from common import use_data


def creation_app_dash(srv_Flask):
    """ Création de l'application Dash pour les diagrammes

    Arguments:
    srv_Flask - le serveur Flask configuré

    Variables:
    df_all - DataFrame contenant toutes les données chargées
    annees_disponibles - liste des années disponibles dans les données
    regions_disponibles - liste des régions disponibles dans les données
    header - en-tête de l'application Dash
    Dropdown_annees - composant Dropdown pour sélectionner l'année
    Dropdown_regions - composant Dropdown pour sélectionner la région
    Diagramme_dep - composant Graph pour le diagramme des passagers au départ
    Diagramme_arr - composant Graph pour le diagramme des passagers à l'arrivée
    Diagramme_tr - composant Graph pour le diagramme des passagers en transit
    Diagramme_camembert - composant Graph pour le diagramme en camembert des 3 types de passagers
    app_Dash.layout - disposition de l'application Dash

    Fonctions:
    update_diagramme - fonction de rappel pour mettre à jour les diagrammes en fonction des sélections

    """
    app_Dash = Dash(__name__, server=srv_Flask, routes_pathname_prefix="/diagramme/", suppress_callback_exceptions=True)

    df_all = use_data.charger_les_data(["2018", "2019", "2020", "2021"])
    df_all["ANNEE"] = df_all["ANMOIS"].astype(str).str[:4] #extraire l'année de la colonne ANMOIS

    annees_disponibles = sorted(df_all["ANNEE"].unique()) #trier les années disponibles
    regions_disponibles = sorted(df_all["REGION"].unique()) #trier les régions disponibles

    header = html.Div(className = 'header', #header de la page
    children = [
    html.Img(src='/static/images/ESIEE_Paris_logo.png', className='logo', alt='ESIEE Paris Logo'),
    html.H1("Diagramme", className = "titre_header_diagramme")
    ])

    Dropdown_annees = html.Div(className="dropdown_annees", #Dropdown pour sélectionner l'année
        children = [
        html.Label("Sélectionner une année:"),
        dcc.Dropdown(
            id="annee_dropdown",
            options=[{"label":str(annee), "value": annee} for annee in annees_disponibles],
            value=annees_disponibles[0]
            )
    ]) 

    Dropdown_regions = html.Div(className="dropdown_regions", #Dropdown pour sélectionner la région
        children = [
        html.Label("Sélectionner une région:"),
        dcc.Dropdown(
            id="region_dropdown",
            options=[{"label":str(region), "value": region} for region in regions_disponibles],
            value=regions_disponibles[0]
            )
    ])

    # Création des graphiques
    Diagramme_dep = dcc.Graph(id= "graphe_diagramme_dep", className="graphe")
    Diagramme_arr = dcc.Graph(id= "graphe_diagramme_arr", className="graphe")
    Diagramme_tr = dcc.Graph(id= "graphe_diagramme_tr", className="graphe")
    Diagramme_camembert = dcc.Graph(id= "graphe_diagramme_camembert", className="graphe")

    # Disposition de l'application Dash
    app_Dash.layout =  html.Div([
    html.Link(rel="stylesheet", href="/static/css/diagramme.css"),
    header,
    Dropdown_annees,
    Dropdown_regions,
    Diagramme_dep,
    Diagramme_arr,
    Diagramme_tr,
    Diagramme_camembert
    ])

    # Callback pour mettre à jour les diagrammes en fonction des sélections
    @app_Dash.callback(
         Output("graphe_diagramme_dep", "figure"),
         Output("graphe_diagramme_arr", "figure"),
         Output("graphe_diagramme_tr", "figure"),
         Output("graphe_diagramme_camembert", "figure"),
         Input("annee_dropdown", "value"),
         Input("region_dropdown", "value")
    )

    def update_diagramme(annee, region):

        """ Met à jour les diagrammes en fonction de l'année et de la région sélectionnées
    
        Arguments:
        annee -- année sélectionnée dans le Dropdown
        region -- région sélectionnée dans le Dropdown

        Returns:
        fig_dep -- figure du diagramme des passagers au départ
        fig_arr -- figure du diagramme des passagers à l'arrivée
        fig_tr -- figure du diagramme des passagers en transit
        fig_camembert -- figure du diagramme en camembert des 3 types de passagers
        
        Variables:
        url - URL de l'API pour récupérer les données filtrées
        resp - réponse de la requête API
        data - données JSON récupérées de l'API
        df_jsonified - DataFrame créé à partir des données JSON
        df_groupe_depart - DataFrame regroupé pour les passagers au départ par mois de l'année sélectionnée
        df_groupe_arrivee - DataFrame regroupé pour les passagers à l'arrivée par mois de l'année sélectionnée
        df_groupe_transit - DataFrame regroupé pour les passagers en transit par mois de l'année sélectionnée
        fig_dep - figure du diagramme des passagers au départ
        fig_arr - figure du diagramme des passagers à l'arrivée
        fig_tr - figure du diagramme des passagers en transit
        total_dep - total des passagers au départ sur l'année sélectionnée
        total_arr - total des passagers à l'arrivée sur l'année sélectionnée
        total_tr - total des passagers en transit sur l'année sélectionnée
        df_camembert - DataFrame pour le diagramme en camembert des 3 types de passagers
        fig_camembert - figure du diagramme en camembert des 3 types de passagers
        
        """
        url = f"http://127.0.0.1:5000/api/data?year={annee}&region={region}"
        resp = requests.get(url)
        data_json = resp.json() #récupérer les données JSON de l'API
        df = pd.DataFrame(data_json) #convertir les données JSON en DataFrame pandas
        df["DATE"] = pd.to_datetime(df["ANMOIS"].astype(str), format="%Y%m") #convertir ANMOIS en format date

        # Regrouper les données par DATE et sommer les passagers
        df_groupe_depart = (df.groupby("DATE", as_index=False)["APT_PAX_dep"].sum())
        df_groupe_arrivee = (df.groupby("DATE", as_index=False)["APT_PAX_arr"].sum())
        df_groupe_transit = (df.groupby("DATE", as_index=False)["APT_PAX_tr"].sum())

        # Créer les figures des diagrammes
        fig_dep = px.bar(
            df_groupe_depart,
            x="DATE",
            y="APT_PAX_dep",
            title=f"Passagers au départ - {region} en ({annee})",
            labels={"APT_PAX_dep": "Passagers au départ"}
        )
        fig_arr = px.bar(
            df_groupe_arrivee,
            x="DATE",
            y="APT_PAX_arr",
            title=f"Passagers à l'arrivée - {region} en ({annee})",
            labels={"APT_PAX_arr": "Passagers à l'arrivée"}
        )
        fig_tr = px.bar(
            df_groupe_transit,
            x="DATE",
            y="APT_PAX_tr",
            title=f"Passagers en transit - {region} en ({annee})",
            labels={"APT_PAX_tr": "Passagers en transit"}
        )

        # Personnalisation des graphiques : thème dark
        fig_dep.update_layout(template="plotly_dark")
        fig_arr.update_layout(template="plotly_dark")
        fig_tr.update_layout(template="plotly_dark")

        # Personnalisation des couleurs des barres
        fig_dep.update_traces(marker_color="deepskyblue")
        fig_arr.update_traces(marker_color="darkgreen")
        fig_tr.update_traces(marker_color="darkorange")

        # Somme des passagers pour l'année sélectionnée
        total_dep = df_groupe_depart["APT_PAX_dep"].sum()
        total_arr = df_groupe_arrivee["APT_PAX_arr"].sum()
        total_tr = df_groupe_transit["APT_PAX_tr"].sum()

        # Préparer les données pour le diagramme en camembert
        df_camembert = pd.DataFrame({
            "Type": ["Départ", "Arrivée", "Transit"],
            "Passagers": [total_dep, total_arr, total_tr]
        })

        # Diagramme en camembert pour la répartition des types de passagers
        fig_camembert = px.pie(
            df_camembert,
            names="Type",
            values="Passagers",
            color= "Type",
            color_discrete_map={
                "Départ": "deepskyblue",
                "Arrivée": "darkgreen",
                "Transit": "darkorange"
            },
            title=f"Répartition des passagers - {region} en ({annee})"
        )

        # Personnalisation du graphique : thème dark
        fig_camembert.update_layout(template="plotly_dark")

        return fig_dep, fig_arr, fig_tr, fig_camembert # Retourner les figures




    

    