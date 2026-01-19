'''
Prend les fichiers dans les data/raw, formatte les données puis les met dans data/clean
'''

import json
import os
import pandas as pd
from common import get_data

def normaliser_an_mois():
    """Normalise la colonne ANMOIS du Dataframe entrée en parametre
    """
    fichiers = [os.path.join("data/clean", f) for f in os.listdir("data/clean")]
    for fichier in fichiers:
        df = pd.read_csv(fichier, sep=";")
        df['ANMOIS'] = df['ANMOIS'].apply(lambda x: str(x)[:4]+ "-" + str(x)[4:])
        df.to_csv(f'data/clean/{fichier.split("/")[2]}', sep=";", index=False)

def ajout_region():
    """ Ajout d'une région pour les aéroport dans le json
    """
    with open("region.json", "r", encoding="utf-8") as f:
        regions = json.load(f)

    fichiers = [os.path.join("data/raw", f) for f in os.listdir("data/raw")]
    for fichier in fichiers:
        df = pd.read_csv(fichier, sep=";")
        df["REGION"] = df["APT_NOM"].map(regions)
        df["REGION"] = df["REGION"].fillna("Inconnue")

        nom_fichier = os.path.basename(fichier)
        df.to_csv(f"data/clean/{nom_fichier}", sep=";", index=False)

def nettoyage_fichier():
    """ Supprime tout les fichiers dans les dossiers data/raw et data/clean
    """
    dossiers = ["data/raw", "data/clean"]
    for dossier in dossiers:
        for fichier in os.listdir(dossier):
            os.remove(os.path.join(dossier, fichier))

def initialiser_donnees():
    """ Télécharge les données puis les formatte et les mets dans le fichier clean
    """
    nettoyage_fichier()
    get_data.charger_donnees()
    normaliser_an_mois()
    ajout_region()
