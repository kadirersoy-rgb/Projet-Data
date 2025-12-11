'''
Prend les fichiers dans les data/raw, formatte les données puis les met dans data/clean
'''

import os, pandas as pd
from common import get_data

def Normaliser_ANMOIS():
    """Normalise la colonne ANMOIS du Dataframe entrée en parametre
    
    Arguments:
    DataFrames -- contient un dataframe de pandas
    """
    fichiers = [os.path.join("data/raw", f) for f in os.listdir("data/raw")]
    for fichier in fichiers:
        df = pd.read_csv(fichier, sep=";")
        df['ANMOIS'] = df['ANMOIS'].apply(lambda x: str(x)[:4]+ "-" + str(x)[4:]) 
        df.to_csv(f'data/clean/{fichier.split("/")[2]}', sep=";", index=False)

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
    get_data.charger_donnees()
    Normaliser_ANMOIS()