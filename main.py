# V0 Start of collaboration : ERSOY-POKRYWA-HONODOU ESIEE Paris E3 FI
#V1 Kadir ERSOY - Lucas POKRYWA - Valentin HONODOU : Creation de l'arborescence du projet
#V2 Kadir ERSOY : Creation du serveur Flask + creation d'un header de page d'accueil (index.html)
from common import server
from common import data

if __name__ == "__main__":
    server.creation_serveur()
    dataframe = data.charger_les_data() #Test chargement data
    DatFrames_Normalized = data.Normaliser_col_ANMOIS_DateTimes(dataframe) #Test normalisation col ANMOIS en DateTime

    print (DatFrames_Normalized['2018']['ANMOIS'])