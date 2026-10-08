'''
Recuperer les données fetch si elles ou prendre les données dans le répertoires
'''
import os
import requests
import zipfile
from common.scrapper import get_zip_link

def telecharger_fichier():
    """ Téléchargement d'un fichier avec un url donné
    """

    r = requests.get(get_zip_link(), timeout=120)
    r.raise_for_status()
    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/data.zip", "wb") as f:
        f.write(r.content)

def unzip_fichier():
    """  Unzip des fichiers, d'un dossier compressé, avec ses années données
    """

    with zipfile.ZipFile("data/raw/data.zip", 'r') as zf:
        for nom in zf.namelist():
            for annee in ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]:
                if annee in nom:
                    zf.extract(nom, "data/raw")
                    os.rename(f'data/raw/{nom}', f'data/raw/{annee}-data.csv')
    os.remove("data/raw/data.zip")

def charger_donnees():
    telecharger_fichier()
    unzip_fichier()
