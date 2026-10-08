import requests
import re
from urllib.parse import urlsplit

def get_zip_link():
    """ Permet de recupérer l'url de téléchargement depuis le lien du site
    """

    api_url = "https://www.data.gouv.fr/api/1/datasets/trafic-aerien-commercial-mensuel-francais-par-paire-daeroports-par-sens-depuis-1990/"

    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        data = response.json()

    except (requests.RequestException, ValueError) as e:
        raise RuntimeError("Impossible de récupérer les ressources du jeu de données.") from e

    archives = []
    for resource in data.get('resources', []):
        match = re.fullmatch(r"ASP_APT_1990_(\d{4})(?:\.zip)?", resource.get('title') or '', re.IGNORECASE)
        if match:
            archives.append((int(match.group(1)), resource))

    for _, resource in sorted(archives, key=lambda item: item[0], reverse=True):
        for url in (resource.get('latest'), resource.get('url')):
            if isinstance(url, str):
                parsed = urlsplit(url)
                if parsed.scheme in ('http', 'https') and parsed.netloc:
                    return url

    raise RuntimeError("Aucune archive ASP_APT_1990 avec une URL valide dans le jeu de données.")
