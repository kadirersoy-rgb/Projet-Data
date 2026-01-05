'''
Module pour définir une API Flask permettant un filtrage dynamique des données
'''

from flask import jsonify, request
from common import use_data

def api(srv_Flask):
    """ Définition de l'API pour le filtrage dynamique des données

    Arguments:
    srv_Flask - le serveur Flask configuré

    Returns:
    df_filtered_json - données JSON converties à partir du DataFrame filtré

    Variables:
    df_all - DataFrame contenant toutes les données chargées
    annee - année sélectionnée dans les paramètres de l'API
    region - région sélectionnée dans les paramètres de l'API
    df_filtered - DataFrame filtré selon l'année et la région et converti en dictionnaire

    """
    df_all = use_data.charger_les_data(["2018", "2019", "2020", "2021"])
    df_all["ANNEE"] = df_all["ANMOIS"].astype(str).str[:4] #extraire l'année de la colonne ANMOIS

    # Définir la route de l'API pour le filtrage des données
    @srv_Flask.route('/api/data')  
    def api_data():

        annee = request.args.get('year', type=str) #récupérer l'année des paramètres de l'API
        region = request.args.get('region', type=str) #récupérer la région des paramètres de l'API

        df_filtered = df_all[(df_all["ANNEE"] == annee) & (df_all["REGION"] == region)] #filtrer le DataFrame selon l'année et la région
        df_filtered = df_filtered.to_dict(orient="records") #convertir le DataFrame filtré en dictionnaire

        df_filtered_json = jsonify(df_filtered) #convertir le dictionnaire en JSON pour la réponse de l'API

        return df_filtered_json #retourner les données JSON filtrées