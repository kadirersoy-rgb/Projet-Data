from dash import Dash, html

def creation_app_dash(srv_Flask):
    app_Dash = Dash(__name__, server=srv_Flask, routes_pathname_prefix="/map/", suppress_callback_exceptions=True)

    annees_disponibles = ["2018", "2019", "2020", "2021"]

    # --- HEADER ---
    header = html.Div(className='header',
        children=[
            html.Img(src='/static/images/ESIEE_Paris_logo.png', className='logo', alt='ESIEE Paris Logo'),
            html.H1("Carte Choroplèthe", className="titre_header_diagramme")
        ]
    )
    
    # Dropdown Années
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

    # Dropdown Type de flux
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
        # Fichier css du diagramme
        html.Link(rel="stylesheet", href="/static/css/diagramme.css"), 
        
        header,
        Dropdown_annees,
        Dropdown_type,
        
        # Ajout de la classe graphe pour le style (marges etc.)
        dcc.Graph(id="map_passagers", className="graphe", style={'height': '80vh'})
    ])

    @app_Dash.callback(
        Output("map_passagers", "figure"),
        Input("filter_year", "value"),
        Input("filter_type_pax", "value")
    )
    def update_map(annee, type_pax_choisi):
        
        # Logique de récupération des données via l'API Flask
        try:
            if type_pax_choisi == 'ALL':
                # Si "ALL", on fait 2 requêtes et on combine les résultats
                url_dep = f"http://127.0.0.1:5000/api/data?year={annee}&type_pax=APT_PAX_dep"
                url_arr = f"http://127.0.0.1:5000/api/data?year={annee}&type_pax=APT_PAX_arr"
                
                r_dep = requests.get(url_dep)
                r_arr = requests.get(url_arr)
                
                df_dep = pd.DataFrame(r_dep.json())
                df_arr = pd.DataFrame(r_arr.json())
                
                # On concatène les deux DataFrames
                df_filtered = pd.concat([df_dep, df_arr])
                
                titre_flux = "du Trafic Total"
            else:
                # Cas standard
                api_url = f"http://127.0.0.1:5000/api/data?year={annee}&type_pax={type_pax_choisi}"
                r = requests.get(api_url)
                df_filtered = pd.DataFrame(r.json())
                
                titre_flux = "des Départs" if type_pax_choisi == "APT_PAX_dep" else "des Arrivées"

            if df_filtered.empty: 
                # Retourne une carte vide avec le thème dark
                empty_fig = px.choropleth(title="Données vides")
                empty_fig.update_layout(template="plotly_dark")
                return empty_fig

        except Exception as e:
            print(f"Erreur: {e}")
            err_fig = px.choropleth(title="Erreur API")
            err_fig.update_layout(template="plotly_dark")
            return err_fig

        # AGRÉGATION
        df_grouped = df_filtered.groupby("REGION")["NB_PASSAGERS"].sum().reset_index()
        
        # Filtre > 0
        df_grouped = df_grouped[df_grouped["NB_PASSAGERS"] > 0] 

        # Calcul du logarithme
        df_grouped["LOG_PAX"] = np.log10(df_grouped["NB_PASSAGERS"])
        # On clip pour éviter d'être hors bornes
        df_grouped["LOG_PAX"] = df_grouped["LOG_PAX"].clip(lower=LOG_MIN, upper=LOG_MAX)

        # Création de la map choroplèthe
        fig = px.choropleth(
            df_grouped,
            geojson=geojson_france,
            locations="REGION",
            featureidkey="properties.nom",
            color="LOG_PAX", 
            range_color=[LOG_MIN, LOG_MAX],
            color_continuous_scale="Viridis", 
            
            hover_name="REGION",
            hover_data={"NB_PASSAGERS": True, "LOG_PAX": False, "REGION": False},
            
            scope="europe",
            title=f"Volume {titre_flux} en {annee} (Échelle Log)",
        )

        fig.update_geos(
            fitbounds="locations", 
            visible=False,
            bgcolor="rgba(0,0,0,0)" # Fond de la carte transparent pour se fondre dans le thème
        )

        fig.update_layout(
            margin={"r":0,"t":50,"l":0,"b":0},
            paper_bgcolor="rgba(0,0,0,0)", # Fond transparent
            geo_bgcolor="rgba(0,0,0,0)",
            coloraxis_colorbar=dict(
                title="Passagers",
                tickvals=[3, 4, 5, 6, 7, 8], 
                ticktext=["1k", "10k", "100k", "1M", "10M", "100M"],
            )
        )

        return fig

    return app_Dash