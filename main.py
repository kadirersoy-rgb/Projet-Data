from common import server, clean_data
from app import dash_diagramme, dash_map
from common import api

if __name__ == "__main__":

    clean_data.initialiser_donnees() #Initialisation des données (téléchargement + nettoyage)
    srv_flask = server.creation_serveur() #Création du serveur Flask
    dash_diagramme.creation_app_dash(srv_flask) #Création de l'application Dash pour les diagrammes
    dash_map.creation_app_dash(srv_flask) #Création de l'application Dash pour la carte
    api.api(srv_flask) #Activation de l'API (pour filtrage dynamique)
    srv_flask.run(host='0.0.0.0', port=5000, debug=True) #Lancement du serveur Flask
