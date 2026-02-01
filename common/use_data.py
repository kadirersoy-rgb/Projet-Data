import os
import pandas as pd
from typing import List

def extraire_donnees(dataframes, donnees: List[str]) -> None:
    """ Extraire les données d'un Dataframe sous forme de tableau

    Arguments:
    dataframes -- un dataframe pandas
    donnees -- tableau des entetes de données voulue ex : ["ANMOIS","APT"]

    Return:
    tableau: jeu de données avec les colonnes voulues
    """
    tableau = dataframes[donnees].values.tolist()
    return tableau


def charger_les_data(annees: List[str]) -> None:
    """Retourne un Dataframe de pandas des fichiers de data

    Arguments:
    annees -- Liste des années voulues de 2018-2021 ex: ["2018","2021"]

    Return:
    df: joint les différents jeu de données avec les differentes années voulues
    """
    projet_folder_data= os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/clean")
    fichiers={}
    dataframes={}

    for annee in annees:
        fichiers[annee] = os.path.join(projet_folder_data, f"{annee}-data.csv")

    for annees, chemin in fichiers.items():
        df = pd.read_csv(chemin, sep=";")
        dataframes[annees] = df

    df = pd.concat(dataframes.values(), ignore_index=True)
    return df
