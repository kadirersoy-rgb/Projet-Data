'''
Recuperer les données fetch si elles ou prendre les données dans le répertoires
'''
import os, requests, zipfile
    
def telecharger_fichier():
    """ Téléchargement d'un fichier avec un url donné

    Arguments:
    chemin_fichier -- Chemin destination du fichier
    url -- url du téléchargement du fichier
    """
    url = "https://www.data.gouv.fr/api/1/datasets/r/ad91ede7-3eb9-41fe-8a00-0324210bfa59"
    r = requests.get(url)
    with open("data/raw/data.zip", "wb") as f:
        f.write(r.content)

def unzip_fichier():
    """  Unzip des fichiers, d'un dossier compressé, avec ses années données

    chemin_fichier -- emplacement de l'archive
    annees -- tableau de string d'années voulu
    """
    with zipfile.ZipFile("data/raw/data.zip", 'r') as zf:
        for nom in zf.namelist():
            for annee in ["2018", "2019", "2020", "2021"]:
                if annee in nom:
                    zf.extract(nom, "data/raw")
                    os.rename(f'data/raw/{nom}', f'data/raw/{annee}-data.csv')
    os.remove("data/raw/data.zip")

def charger_donnees():
    telecharger_fichier()
    unzip_fichier()