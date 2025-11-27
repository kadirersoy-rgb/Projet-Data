'''
Contenu du serveur web
'''
from flask import Flask

def creation_serveur():
    app = Flask(__name__)

    @app.route('/')
    def welcome():
        return 'Hello, World!' \
        
    app.run(host='0.0.0.0', port=5000, debug=True)
