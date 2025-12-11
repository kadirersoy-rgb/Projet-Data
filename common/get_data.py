'''
Recuperer les données fetch si elles ou prendre les données dans le répertoires
'''
import pandas as pd
import os
from typing import List
import requests 
import zipfile

def charger_les_data(annees: List[str]) -> None:
    """Retourne un Dataframe de pandas des fichiers de data

    Arguments:
    annees -- Liste des années voulues de 2018-2021 ex: ["2018","2021"]
    """
    
    projet_folder_data= os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    fichiers={}
    Dataframes={}

    for annee in annees:
        fichiers[annee] = os.path.join(projet_folder_data, f"{annee}-data.csv")

    for annees, chemin in fichiers.items():
        df = pd.read_csv(chemin, sep=";")
        Dataframes[annees] = df

    return Dataframes
    
def Normaliser_ANMOIS(DataFrames):
    """Normalise la colonne ANMOIS du Dataframe entrée en parametre
    
    Arguments:
    DataFrames -- contient un dataframe de pandas
    """

    conversion = {}
    for annees, df in DataFrames.items():
        df = df.copy()
        df['ANMOIS'] = df['ANMOIS'].apply(lambda x: str(x)[:4]+ "-" + str(x)[4:]) 
        conversion[annees] = df
    return conversion

def telecharger_fichier(chemin_fichier, url):
    """ Téléchargement d'un fichier avec un url donné

    Arguments:
    chemin_fichier -- Chemin destination du fichier
    url -- url du téléchargement du fichier
    """
    r = requests.get(url)
    with open(chemin_fichier, "wb") as f:
        f.write(r.content)

def unzip_fichier(chemin_fichier, annees):
    """  Unzip des fichiers, d'un dossier compressé, avec ses années données

    chemin_fichier -- emplacement de l'archive
    annees -- tableau de string d'années voulu
    """
    with zipfile.ZipFile(chemin_fichier, 'r') as zf:
        for nom in zf.namelist():
            for annee in annees:
                if annee in nom:
                    zf.extract(nom, "data")
                    os.rename(f'data/{nom}', f'data/{annee}-data.csv')
    os.remove(chemin_fichier)
