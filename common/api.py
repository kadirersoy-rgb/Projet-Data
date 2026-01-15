"""
Module pour définir une API Flask permettant un filtrage dynamique des données
"""

from flask import jsonify, request
from common import use_data
import pandas as pd

def api(srv_Flask):
    """ Définition de l'API pour le filtrage dynamique des données

    Arguments:
    srv_Flask - le serveur Flask configuré

    Returns:
    df_filtered_json - données JSON converties à partir du DataFrame filtré
    """
    # Chargement unique des données au démarrage
    df_all = use_data.charger_les_data(["2018", "2019", "2020", "2021"])
    df_all["ANNEE"] = df_all["ANMOIS"].astype(str).str[:4] # Extraire l'année

    # Définir la route de l'API pour le filtrage des données
    @srv_Flask.route('/api/data')
    def api_data():

        # Récupération des paramètres
        annee = request.args.get('year', type=str)
        region = request.args.get('region', type=str)      # Optionnel (pour le diagramme)
        type_pax = request.args.get('type_pax', type=str)  # Optionnel (pour la map : APT_PAX_arr ou APT_PAX_dep)

        # J'utilse une copie pour ne pas modifier l'original
        df_filtered = df_all.copy()

        # Filtrage par Année (Obligatoire)
        if annee:
            df_filtered = df_filtered[df_filtered["ANNEE"] == annee]

        # Filtrage par Région
        if region:
            df_filtered = df_filtered[df_filtered["REGION"] == region]

        # Gestion du Type de Flux de Passagers
        if type_pax:
            if type_pax in df_filtered.columns:
                # Je renomme la colonne spécifique (ex: APT_PAX_dep) en "NB_PASSAGERS"
                # Comme ça, Dash utilise toujours la même clé "NB_PASSAGERS"
                df_filtered = df_filtered.rename(columns={type_pax: "NB_PASSAGERS"})

        df_filtered_dict = df_filtered.to_dict(orient="records")
        return jsonify(df_filtered_dict)

    return df_all 