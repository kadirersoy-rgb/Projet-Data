'''
Module pour créer une application Dash affichant une carte choroplèthe interactive des flux de passagers
'''
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import json
import requests
import numpy as np

# Chargement du GeoJSON contenant les contours des régions françaises
with open('common/regions.geojson', 'r') as f:
    geojson_france = json.load(f)

DOM_TOM = ["La Réunion", "Guadeloupe", "Martinique", "Guyane", "Mayotte"]

# Bornes constante pour l'échelle de couleur logarithmique
# Pour une échelle de couleur cohérente entre les années et types de flux
LOG_MIN = 5.0   # environ 100k passagers
LOG_MAX = 7.7   # environ 50M passagers

# Bornes pour le flux de transit (plus faible)
TRANSIT_LOG_MIN = 2.3  # environ 200 passagers
TRANSIT_LOG_MAX = 4.9  # environ 80k passagers

def creation_app_dash(srv_flask):
    """ Création de l'application Dash pour la visualisation cartographique
    Arguments:
    srv_flask - le serveur Flask configuré
    """

    app_dash = Dash(__name__, server=srv_flask, routes_pathname_prefix="/map/", suppress_callback_exceptions=True)

    annees_disponibles = ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]

    # --- HEADER ---
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
            html.H1("Carte Choroplèthe", className="titre_header_diagramme"),
            html.A(
                href="/",
                children=html.Button("Accueil", className="button_home"),
                className="button_home_lien"
            )
        ],
        className='header'
    )

    # --- FILTRES ---
    dropdown_annees = html.Div(className="dropdown_annees", #Dropdown pour sélectionner l'année
        children=[
            html.Label("Sélectionner une année :"),
            dcc.Dropdown(
                id="filter_year",
                options=[{"label": str(a), "value": a} for a in annees_disponibles],
                value="2018", # Valeur par défaut
                clearable=False
            )
        ]
    )

    dropdown_type = html.Div(className="dropdown_regions", #Dropdown pour sélectionner le type de flux
        children=[
            html.Label("Type de flux :"),
            dcc.Dropdown(
                id="filter_type_pax",
                options=[
                    {'label': 'Départ', 'value': 'APT_PAX_dep'},
                    {'label': 'Arrivée', 'value': 'APT_PAX_arr'},
                    {'label': 'Total (Départ + Arrivée)', 'value': 'ALL'},
                    {'label': 'Transit', 'value': 'APT_PAX_tr'}
                ],
                value='ALL', # Valeur par défaut
                clearable=False
            )
        ]
    )

    # --- LAYOUT ---
    # Disposition de l'application Dash
    app_dash.layout = html.Div([
        html.Link(rel="stylesheet", href="/static/css/diagramme.css"),
        header,
        html.Div([dropdown_annees, dropdown_type], style={'display': 'flex', 'gap': '20px', 'padding': '20px'}),

        # Carte Métropole
        html.Div([
            html.H3("France Métropolitaine", style={'textAlign': 'center'}),
            dcc.Graph(
                id="map-metro",
                className="graphe",
                config={'scrollZoom': False, 'displayModeBar': False},
                style={'height': '600px'}
            )
        ]),

        html.Hr(style={'margin': '30px 0'}), # Séparateur visuel

        # Cartes DOM-TOM
        html.Div([
            html.H3("Outre-mer", style={'textAlign': 'center'}),
            html.Div(
                id="map-dom-container",
                style={'display': 'flex', 'justify-content': 'center', 'flex-wrap': 'wrap', 'gap': '10px'}
            )
        ])
    ])

    # --- CALLBACK ---
    # CallBack pour la mise à jour des cartes en fonction des filtres sélectionnés
    @app_dash.callback(
        [Output('map-metro', 'figure'),
         Output('map-dom-container', 'children')],
        [Input('filter_year', 'value'),
         Input('filter_type_pax', 'value')]
    )
    def update_maps(selected_year, selected_pax):
        """ Met à jour les cartes en fonction de l'année et du type de flux sélectionnés
        Arguments:
        selected_year - l'année sélectionnée
        selected_pax - le type de flux sélectionné
        Retourne:
        fig_metro - la figure de la carte métropole mise à jour
        dom_figures - la liste des figures des cartes DOM-TOM mises à jour
        """

        # Requête à l'API pour obtenir les données filtrées
        url = "http://127.0.0.1:5000/api/data"
        params = {'year': selected_year, 'type_pax': selected_pax}

        try:
            response = requests.get(url, params=params)
            data = response.json() # Récupération des données JSON de l'API
            df = pd.DataFrame(data) # Conversion du JSON en DataFrame avec pandas
        except Exception as e:
            print(f"Erreur API: {e}")
            return {}, []

        if df.empty:
            return {}, []


        # Choix de l'échelle selon le type de flux
        if selected_pax == "APT_PAX_tr":
            log_min = TRANSIT_LOG_MIN
            log_max = TRANSIT_LOG_MAX
            colorbar_ticks = {
                "tickvals": [2, 3, 4, 5],
                "ticktext": ["100", "1k", "10k", "100k"]
            }
        else:
            log_min = LOG_MIN
            log_max = LOG_MAX
            colorbar_ticks = {
                "tickvals": [3, 4, 5, 6, 7, 8],
                "ticktext": ["1k", "10k", "100k", "1M", "10M", "100M"]
    }


        # Préparation des données
        # Regrouper par région et sommer les passagers
        df_map = df.groupby("REGION", as_index=False)["NB_PASSAGERS"].sum()
        df_map = df_map[df_map["NB_PASSAGERS"] > 0]

        # Calculer le logarithme des passagers
        df_map["LOG_PAX"] = np.log10(df_map["NB_PASSAGERS"])
        df_map["LOG_PAX"] = df_map["LOG_PAX"].clip(lower=log_min, upper=log_max)


        # Formatage des passagers pour le hover
        # Exemple: 1234567 -> 1 234 567
        df_map["PAX_FMT"] = df_map["NB_PASSAGERS"].apply(lambda x: "{:,}".format(int(x)).replace(",", " "))

        # Séparation Métropole / DOM-TOM
        df_metro = df_map[~df_map["REGION"].isin(DOM_TOM)]

        # --- CARTE MÉTROPOLE ---
        fig_metro = px.choropleth(
            df_metro,
            geojson=geojson_france,
            locations="REGION",
            featureidkey="properties.nom",
            color="LOG_PAX",
            # range_color=[LOG_MIN, LOG_MAX], # Fixer l'échelle de couleur
            range_color=[log_min, log_max],
            color_continuous_scale="Viridis",
            # Choix des données dont on a besoin pour le survol
            custom_data=["REGION", "PAX_FMT"]
        )

        # Format personnalisé pour le hover
        # %{customdata[0]} -> REGION (nom de la région)
        # %{customdata[1]} -> PAX_FMT (nombre de passagers)
        fig_metro.update_traces(
            hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]} passagers<extra></extra>"
        )

        # Ajustements de la carte et du layout
        fig_metro.update_geos(
            projection_type="mercator", # Important pour ne pas déformer la carte
            fitbounds="locations",
            visible=False
        )

        fig_metro.update_layout(
            dragmode=False,
            margin={"r":0,"t":0,"l":0,"b":0},
            coloraxis_showscale=True,
            # Légende personnalisée pour l'échelle logarithmique
            coloraxis_colorbar=dict(
                title="Passagers",
                **colorbar_ticks
            )
        )

        # --- CARTES DOM-TOM ---
        dom_figures = []
        for region_name in DOM_TOM:
            df_region = df_map[df_map["REGION"] == region_name]

            if df_region.empty:
                continue

            # Création d'une carte individuelle pour chaque DOM-TOM
            fig_dom = px.choropleth(
                df_region,
                geojson=geojson_france,
                locations="REGION",
                featureidkey="properties.nom",
                color="LOG_PAX",
                # range_color=[LOG_MIN, LOG_MAX],
                range_color=[log_min, log_max],
                color_continuous_scale="Viridis",
                custom_data=["REGION", "PAX_FMT"],
                title=region_name
            )

            fig_dom.update_traces(
                hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]} passagers<extra></extra>"
            )

            fig_dom.update_geos(fitbounds="locations", visible=False)
            fig_dom.update_layout(
                dragmode=False,
                margin={"r":0,"t":30,"l":0,"b":0},
                coloraxis_showscale=False, # Masquer l'échelle de couleur pour les DOM-TOM
                height=300,
                title_font_size=12
            )

            # Ajouter la figure DOM-TOM à la liste
            dom_figures.append(
                html.Div(
                    dcc.Graph(figure=fig_dom, config={'scrollZoom': False, 'displayModeBar': False}),
                    style={'width': '250px', 'display': 'inline-block'}
                )
            )

        return fig_metro, dom_figures # Retourne la figure métropole et les figures DOM-TOM

    return app_dash # Retourne l'application Dash créée
