"""
Module pour créer une application Dash affichant des diagrammes comparatifs
entre deux régions
"""

from dash import Dash, html, dcc, Input, Output
import requests
import plotly.express as px
import pandas as pd
from common import use_data


def creation_app_dash_comparaison(srv_flask):
    """ Création de l'application Dash pour comparer deux régions """

    app_dash = Dash(
        __name__,
        server=srv_flask,
        routes_pathname_prefix="/comparaison/",
        suppress_callback_exceptions=True
    )

    # Chargement des données globales (pour récupérer la liste des régions)
    df_all = use_data.charger_les_data(
        ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]
    )

    regions_disponibles = sorted(df_all["REGION"].unique()) #trier les régions disponibles

    header = html.Div(
        [
            html.A(
                html.Img(
                    src='/static/images/ESIEE_Paris_logo.png',
                    className='logo',
                    alt='ESIEE Paris Logo'
                ),
                href="/",
                className="logo_lien"
            ),
            html.H1("Comparaison de deux régions", className="titre_header_diagramme"),
            html.A(
                href="/",
                children=html.Button("Accueil", className="button_home"),
                className="button_home_lien"
            )
        ],
        className='header'
    )

    # Dropdown pour sélectionner la première région
    dropdown_region_1 = html.Div(
        className="dropdown_regions",
        children=[
            html.Label("Sélectionner la 1ère région :"),
            dcc.Dropdown(
                id="region_1_dropdown",
                options=[{"label": r, "value": r} for r in regions_disponibles],
                value=regions_disponibles[0]
            )
        ]
    )

    # Dropdown pour sélectionner la deuxième région
    dropdown_region_2 = html.Div(
        className="dropdown_regions",
        children=[
            html.Label("Sélectionner la 2e région :"),
            dcc.Dropdown(
                id="region_2_dropdown",
                options=[{"label": r, "value": r} for r in regions_disponibles],
                value=regions_disponibles[1] if len(regions_disponibles) > 1 else regions_disponibles[0]
            )
        ]
    )

    # Création des graphiques
    diagramme_dep = dcc.Graph(id="graphe_compare_dep", className="graphe")
    diagramme_arr = dcc.Graph(id="graphe_compare_arr", className="graphe")
    diagramme_tr = dcc.Graph(id="graphe_compare_tr", className="graphe")

    # Disposition de l'application Dash
    app_dash.layout = html.Div([
        html.Link(rel="stylesheet", href="/static/css/diagramme.css"),
        header,
        dropdown_region_1,
        dropdown_region_2,
        diagramme_dep,
        diagramme_arr,
        diagramme_tr
    ])

    # Callbacks pour mettre à jour les diagrammes en fonction des régions sélectionnées
    @app_dash.callback(
        Output("graphe_compare_dep", "figure"),
        Output("graphe_compare_arr", "figure"),
        Output("graphe_compare_tr", "figure"),
        Input("region_1_dropdown", "value"),
        Input("region_2_dropdown", "value")
    )

    def update_comparaison(region_1, region_2):
        """ Met à jour les diagrammes comparatifs entre deux régions par année """

        def get_df_region(region):
            url = f"http://127.0.0.1:5000/api/data?region={region}"
            resp = requests.get(url)
            data_json = resp.json() # Récupérer les données JSON de l'API
            df = pd.DataFrame(data_json) # Convertir les données JSON en DataFrame pandas

            df["ANNEE"] = df["ANMOIS"].astype(str).str[:4] # Extraire l'année de la colonne ANMOIS

            # Groupes par année
            df_group = df.groupby("ANNEE", as_index=False).agg({
                "APT_PAX_dep": "sum",
                "APT_PAX_arr": "sum",
                "APT_PAX_tr": "sum"
            })

            return df_group

        df_r1 = get_df_region(region_1) # Données de la région 1
        df_r2 = get_df_region(region_2) # Données de la région 2

        def build_long_df(col):
            df1 = df_r1[["ANNEE", col]].copy()
            df1["Région"] = region_1
            df1 = df1.rename(columns={col: "Passagers"})

            df2 = df_r2[["ANNEE", col]].copy()
            df2["Région"] = region_2
            df2 = df2.rename(columns={col: "Passagers"})

            return pd.concat([df1, df2], ignore_index=True)

        df_dep = build_long_df("APT_PAX_dep")   # Données pour les passagers au départ
        df_arr = build_long_df("APT_PAX_arr")   # Données pour les passagers à l'arrivée
        df_tr = build_long_df("APT_PAX_tr")     # Données pour les passagers en transit

        # Création des figures comparatives
        fig_dep = px.bar(
            df_dep,
            x="ANNEE",
            y="Passagers",
            color="Région",
            barmode="group",
            title="Passagers au départ par année (Région 1 vs Région 2)",
            labels={"ANNEE": "Année"}
        )

        fig_arr = px.bar(
            df_arr,
            x="ANNEE",
            y="Passagers",
            color="Région",
            barmode="group",
            title="Passagers à l’arrivée par année (Région 1 vs Région 2)",
            labels={"ANNEE": "Année"}
        )

        fig_tr = px.bar(
            df_tr,
            x="ANNEE",
            y="Passagers",
            color="Région",
            barmode="group",
            title="Passagers en transit par année (Région 1 vs Région 2)",
            labels={"ANNEE": "Année"}
        )

        return fig_dep, fig_arr, fig_tr

    return app_dash
