'''
Module pour créer et configurer le serveur Flask
'''
from flask import Flask, render_template
import os

def creation_serveur():
    """ Création et configuration du serveur Flask
    
    Returns:
    srv_Flask - le serveur Flask configuré

    Variables:
    projet_folder_base - chemin du dossier racine du projet
    projet_folder_static - chemin du dossier static
    projet_folder_templates - chemin du dossier templates

    """
    projet_folder_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    projet_folder_static = os.path.join(projet_folder_base, "static")
    projet_folder_templates = os.path.join(projet_folder_static, "templates")
    
    # Création du serveur Flask avec les dossiers templates et static configurés
    srv_Flask = Flask(__name__, template_folder=projet_folder_templates, static_folder=projet_folder_static) 

    # Définir la route pour la page d'accueil
    @srv_Flask.route('/')
    def index():
        return render_template('index.html')

    return srv_Flask #retourner le serveur Flask configuré
    