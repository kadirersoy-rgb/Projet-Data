'''
Recuperer les données fetch si elles ou prendre les données dans le répertoires
'''
import pandas as pd
import os
from typing import List


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