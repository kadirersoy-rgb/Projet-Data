from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import json
import requests
import numpy as np

# Chargement du GeoJSON
with open('common/regions.geojson', 'r') as f:
    geojson_france = json.load(f)

DOM_TOM = ["La Réunion", "Guadeloupe", "Martinique", "Guyane", "Mayotte"]

# Bornes constante pour l'échelle de couleur logarithmique
# Pour une échelle de couleur cohérente entre les années et types de flux
LOG_MIN = 5.0   # environ 100k passagers
LOG_MAX = 7.7   # environ 50M passagers

def creation_app_dash(srv_Flask):
    app_Dash = Dash(__name__, server=srv_Flask, routes_pathname_prefix="/map/", suppress_callback_exceptions=True)

    annees_disponibles = ["2018", "2019", "2020", "2021"]

    # --- HEADER ---
    header = html.Div(
        [
            html.A(
                html.Img(src='/static/images/ESIEE_Paris_logo.png', className='logo', alt='ESIEE Paris Logo'),
                href="/",
                className="logo_lien"
            ),
            html.H1("Carte Choroplèthe", className="titre_header_diagramme")
        ],
        className='header'
    )
    
    # --- FILTRES ---
    Dropdown_annees = html.Div(className="dropdown_annees",
        children=[
            html.Label("Sélectionner une année :"),
            dcc.Dropdown(
                id="filter_year",
                options=[{"label": str(a), "value": a} for a in annees_disponibles],
                value="2018",
                clearable=False
            )
        ]
    )

    Dropdown_type = html.Div(className="dropdown_regions",
        children=[
            html.Label("Type de flux :"),
            dcc.Dropdown(
                id="filter_type_pax",
                options=[
                    {'label': 'Départ', 'value': 'APT_PAX_dep'},
                    {'label': 'Arrivée', 'value': 'APT_PAX_arr'},
                    {'label': 'Total (Départ + Arrivée)', 'value': 'ALL'} 
                ],
                value='ALL', 
                clearable=False
            )
        ]
    )

    # --- LAYOUT ---
    app_Dash.layout = html.Div([
        html.Link(rel="stylesheet", href="/static/css/diagramme.css"), 
        header,
        html.Div([Dropdown_annees, Dropdown_type], style={'display': 'flex', 'gap': '20px', 'padding': '20px'}),
        
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

        html.Hr(style={'margin': '30px 0'}), 

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
    @app_Dash.callback(
        [Output('map-metro', 'figure'),
         Output('map-dom-container', 'children')],
        [Input('filter_year', 'value'),
         Input('filter_type_pax', 'value')]
    )
    def update_maps(selected_year, selected_pax):
        url = "http://127.0.0.1:5000/api/data"
        params = {'year': selected_year, 'type_pax': selected_pax}
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            df = pd.DataFrame(data)
        except Exception as e:
            print(f"Erreur API: {e}")
            return {}, [] 
        
        if df.empty:
            return {}, []
        
        # 1. Préparation des données
        df_map = df.groupby("REGION", as_index=False)["NB_PASSAGERS"].sum()
        df_map = df_map[df_map["NB_PASSAGERS"] > 0]
        
        df_map["LOG_PAX"] = np.log10(df_map["NB_PASSAGERS"])
        df_map["LOG_PAX"] = df_map["LOG_PAX"].clip(lower=LOG_MIN, upper=LOG_MAX)
        
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
            range_color=[LOG_MIN, LOG_MAX], 
            color_continuous_scale="Viridis",
            # Choix des données dont on a besoin pour le survol
            custom_data=["REGION", "PAX_FMT"] 
        )

        # Format personnalisé pour le hover
        # %{customdata[0]} -> REGION
        # %{customdata[1]} -> PAX_FMT
        # <extra></extra> -> Supprime la boîte "trace 0"
        fig_metro.update_traces(
            hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]} passagers<extra></extra>"
        )

        fig_metro.update_geos(fitbounds="locations", visible=False)
        fig_metro.update_layout(
            dragmode=False, 
            margin={"r":0,"t":0,"l":0,"b":0},
            coloraxis_showscale=True,
            coloraxis_colorbar=dict(
                title="Passagers",
                tickvals=[3, 4, 5, 6, 7, 8], 
                ticktext=["1k", "10k", "100k", "1M", "10M", "100M"],
            )
        )

        # --- CARTES DOM-TOM ---
        dom_figures = []
        for region_name in DOM_TOM:
            df_region = df_map[df_map["REGION"] == region_name]
            
            if df_region.empty:
                continue
                
            fig_dom = px.choropleth(
                df_region,
                geojson=geojson_france,
                locations="REGION",
                featureidkey="properties.nom",
                color="LOG_PAX",
                range_color=[LOG_MIN, LOG_MAX], 
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
                coloraxis_showscale=False, 
                height=300, 
                title_font_size=12
            )
            
            dom_figures.append(
                html.Div(
                    dcc.Graph(figure=fig_dom, config={'scrollZoom': False, 'displayModeBar': False}), 
                    style={'width': '250px', 'display': 'inline-block'}
                )
            )

        return fig_metro, dom_figures

    return app_Dash