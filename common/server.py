'''
Module pour créer et configurer le serveur Flask
'''
from flask import Flask, render_template
import os

def creation_serveur():
    """ Création et configuration du serveur Flask
    Returns:
    srv_Flask - le serveur Flask configuré
    """
    projet_folder_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    projet_folder_static = os.path.join(projet_folder_base, "static")
    projet_folder_templates = os.path.join(projet_folder_static, "templates")

    srv_flask = Flask(__name__, template_folder=projet_folder_templates, static_folder=projet_folder_static)

    @srv_flask.route('/')
    def index():
        return render_template('index.html')

    return srv_flask
