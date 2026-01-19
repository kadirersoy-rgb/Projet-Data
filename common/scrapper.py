import requests

def get_zip_link():
    """ Permet de recupérer l'url de téléchargement depuis le lien du site
    """

    api_url = "https://www.data.gouv.fr/api/1/datasets/trafic-aerien-commercial-mensuel-francais-par-paire-daeroports-par-sens-depuis-1990/"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        for resource in data.get('resources', []):
            if "ASP_APT_1990_2024" in resource.get('title', ''):
                return resource.get('latest') or resource.get('url')

        return "Ressource non trouvée dans le jeu de données."
    except Exception as e:
        return f"Erreur : {e}"
