'''
Contenu du serveur web
'''
from flask import Flask, render_template, jsonify, request
from dash import Dash, html
import os

def creation_serveur():
    projet_folder_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    projet_folder_static = os.path.join(projet_folder_base, "static")
    projet_folder_templates = os.path.join(projet_folder_static, "templates")
    
    srv_Flask = Flask(__name__, template_folder=projet_folder_templates, static_folder=projet_folder_static)

    @srv_Flask.route('/')
    def index():
        return render_template('index.html')

    return srv_Flask
    