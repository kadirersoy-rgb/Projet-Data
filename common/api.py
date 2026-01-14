'''
Module pour définir une API Flask permettant un filtrage dynamique des données
'''

from flask import jsonify, request
import pandas as pd  # Ajout nécessaire pour pd.to_numeric
from common import use_data

def api(srv_Flask):
    """ Définition de l'API pour le filtrage dynamique des données """
    
    # Chargement unique au lancement
    df_all = use_data.charger_les_data(["2018", "2019", "2020", "2021"])
    df_all["ANNEE"] = df_all["ANMOIS"].astype(str).str[:4]

    # Pré-traitement des colonnes numériques (fait une seule fois ici pour optimiser)
    df_all['APT_PAX_dep'] = pd.to_numeric(df_all['APT_PAX_dep'], errors='coerce').fillna(0)
    df_all['APT_PAX_arr'] = pd.to_numeric(df_all['APT_PAX_arr'], errors='coerce').fillna(0)

    @srv_Flask.route('/api/data')  
    def api_data():
        annee = request.args.get('year', type=str)
        region = request.args.get('region', type=str)
        # 1. Récupération du type de passager (par défaut 'dep' si non spécifié)
        type_pax = request.args.get('type_pax', type=str, default='APT_PAX_dep') 

        # Filtrage par année
        mask = (df_all["ANNEE"] == annee)

        # Filtrage par région (optionnel)
        if region:
            mask = mask & (df_all["REGION"] == region)

        # Création d'une copie pour éviter les avertissements pandas
        df_filtered = df_all[mask].copy()

        # 2. Filtrage "Logique" par colonne : 
        # On crée une colonne générique 'NB_PASSAGERS' qui prend la valeur demandée.
        # Cela simplifie le travail de Dash qui n'aura qu'à lire 'NB_PASSAGERS'.
        if type_pax == 'APT_PAX_arr':
            df_filtered['NB_PASSAGERS'] = df_filtered['APT_PAX_arr']
        else:
            df_filtered['NB_PASSAGERS'] = df_filtered['APT_PAX_dep']
            
        # On peut ne renvoyer que les colonnes utiles pour alléger le JSON
        colonnes_a_garder = ['ANNEE', 'REGION', 'NB_PASSAGERS']
        df_dict = df_filtered[colonnes_a_garder].to_dict(orient="records")

        return jsonify(df_dict)