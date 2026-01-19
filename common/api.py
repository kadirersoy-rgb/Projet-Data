"""
Module pour définir une API Flask permettant un filtrage dynamique des données
"""

from flask import jsonify, request
from common import use_data

def api(srv_Flask):
    """ Définition de l'API pour le filtrage dynamique des données

    Arguments:
    srv_Flask - le serveur Flask configuré

    Returns:
    df_filtered_json - données JSON converties à partir du DataFrame filtré
    """
    # Chargement unique des données au démarrage
    df_all = use_data.charger_les_data(["2018", "2019", "2020", "2021", "2022", "2023", "2024"])
    df_all["ANNEE"] = df_all["ANMOIS"].astype(str).str[:4]

    # Définition de la route API
    @srv_Flask.route('/api/data')
    def api_data():

        # Récupération des paramètres de la requête
        annee = request.args.get('year', type=str)
        region = request.args.get('region', type=str)
        type_pax = request.args.get('type_pax', type=str)

        # J'utilise une copie pour le filtrage sans modifier l'original
        df_filtered = df_all.copy()

        # Filtrages
        if annee:
            df_filtered = df_filtered[df_filtered["ANNEE"] == annee]
        if region:
            df_filtered = df_filtered[df_filtered["REGION"] == region]

        # Calcul de la colonne NB_PASSAGERS
        if type_pax == 'ALL' or not type_pax:
            # Addition des deux colonnes
            df_filtered["NB_PASSAGERS"] = (
                df_filtered["APT_PAX_dep"].fillna(0) +
                df_filtered["APT_PAX_arr"].fillna(0)
            )
        elif type_pax in df_filtered.columns:
            # Renommer la colonne en NB_PASSAGERS
            df_filtered = df_filtered.rename(columns={type_pax: "NB_PASSAGERS"})
        else:
            df_filtered["NB_PASSAGERS"] = 0

        return jsonify(df_filtered.to_dict(orient="records"))

    return df_all
