'''
Recuperer les données fetch si elles ou prendre les données dans le répertoires
'''
import pandas as pd
import os

def charger_les_data():

    projet_folder_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    projet_folder_data= os.path.join(projet_folder_base, "data")
    projet_file_data_2018csv = os.path.join(projet_folder_data, "2018-data.csv")
    projet_file_data_2019csv = os.path.join(projet_folder_data, "2019-data.csv")
    projet_file_data_2020csv = os.path.join(projet_folder_data, "2020-data.csv")
    projet_file_data_2021csv = os.path.join(projet_folder_data, "2021-data.csv")

    fichiers = {
        "2018": projet_file_data_2018csv,
        "2019": projet_file_data_2019csv,
        "2020": projet_file_data_2020csv,
        "2021": projet_file_data_2021csv
    }
    DataFrames ={}
    for annees, chemin in fichiers.items():
        df = pd.read_csv(chemin, sep=';')
        DataFrames[annees] = df
    return DataFrames
    
def Normaliser_col_ANMOIS_DateTimes(DataFrames):
    Conversion_DateTimes = {}

    for annees, df in DataFrames.items():
        df = df.copy()
        df['ANMOIS'] = pd.to_datetime(df['ANMOIS'], format='%Y%m')

        Conversion_DateTimes[annees] = df
    return Conversion_DateTimes
   
   