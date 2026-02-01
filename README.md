## 📋 Sommaire

- [A propos](#a-propos)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Documentation](#documentation)

## ℹ️ A propos

Projet Multidisciplinaire de visualisation de données n°1.
Récupération et comparaison des données d'aviation francaise durant la période de 2018 à 2024

## 💾 Installation

Utiliser la commande suivante pour télécharger les dépendances nécéssaires.
Veuillez bien avoir installé [Python](https://www.python.org/downloads/) ainsi que [PiP](https://pip.pypa.io/en/stable/) au préalable

```bash
pip install -r requirements.txt
```

## 🚀 Utilisation

Pour lancer le projet il suffit d'éxécuter la commande suivante :  

```bash
python main.py
```

## 📁 Documentation

#### <u>Arborescence du projet</u>

```bash
.
├── app
│   ├── dash_compare.py
│   ├── dash_diagramme.py
│   └── dash_map.py
├── common
│   ├── api.py
│   ├── clean_data.py
│   ├── get_data.py
│   ├── regions.geojson
│   ├── scrapper.py
│   ├── server.py
│   └── use_data.py
├── data
│   ├── clean
│   │   └── 20**-data.csv
│   └── raw
│       └── 20**-data.csv
├── data_info.png
├── README.md
├── main.py
├── region.json
├── requirements.txt
├── ruff.toml
└── static
    ├── css
    │   ├── diagramme.css
    │   └── index.css
    ├── images
    │   └── ESIEE_Paris_logo.png
    └── templates
        └── index.html
```

#### <u>Utilité des dossiers</u>

**/common** : Utilitaires (récupération, nettoyage, traitement). \
**/data** : Stockage des CSV (sous-dossiers `/raw` et `/clean`). \
**/static** : Assets statiques pour le rendu web. \
**/app** : Logique et interface de l'application Dash. \

## 👥 Auteurs
- Lucas Pokrywa
- Kadir Ersoy
- Valentin Hodonou
- Étudiants à **ESIEE Paris**