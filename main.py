from common import server, api
from app import dash_diagramme, dash_map


if __name__ == "__main__":
    srv_flask = server.creation_serveur()
    dash_diagramme.creation_app_dash(srv_flask)
    dash_map.creation_app_dash(srv_flask)

   # api.get_data(srv_flask) #Activation de l'API (pour filtrage dynamique)

    srv_flask.run(host='0.0.0.0', port=5000, debug=True)