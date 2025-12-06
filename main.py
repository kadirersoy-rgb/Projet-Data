from common import server
from app import dash1
from common import data

if __name__ == "__main__":
    srv_flask = server.creation_serveur()
    dash1.creation_app_dash(srv_flask)

    srv_flask.run(host='0.0.0.0', port=5000, debug=True)
   


   # dataframe = data.charger_les_data() #Test chargement data
   # DatFrames_Normalized = data.Normaliser_col_ANMOIS_DateTimes(dataframe) #Test normalisation col ANMOIS en DateTime

   # print (DatFrames_Normalized['2018']['ANMOIS'])