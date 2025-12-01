'''
Contenu du serveur web
'''
from flask import Flask
from flask import render_template
import os

def creation_serveur():
    projet_folder_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    projet_folder_templates = os.path.join(projet_folder_base, "templates")
    projet_folder_static = os.path.join(projet_folder_base, "static")

    app = Flask(__name__, template_folder=projet_folder_templates, static_folder=projet_folder_static)

    @app.route('/')
    def index():
        return render_template('index.html')
        
    app.run(host='0.0.0.0', port=5000, debug=True)
