'''
Contenu du serveur web
'''
from flask import Flask
from flask import render_template
from dash import Dash
import os

projet_folder_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
projet_folder_templates = os.path.join(projet_folder_base, "templates")
projet_folder_static = os.path.join(projet_folder_base, "static")

def creation_serveur():
    srv_Flask = Flask(__name__, template_folder=projet_folder_templates, static_folder=projet_folder_static)
    #app_Dash = Dash(__name__, serveur=srv_Flask, url_base="/dash/", suppress_callback_exceptions=True)

    @srv_Flask.route('/')
    def index():
        return render_template('index.html')
        
    srv_Flask.run(host='0.0.0.0', port=5000, debug=True)
