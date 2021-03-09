"""Ce module permet d'accéder à proprement parler à l'application se trouvant sur le serveur"""
# -*- coding: utf-8 -*-

import os

from flask import abort, Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from file_manager import *
from login import *


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "./static/temp"
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.secret_key = os.urandom(24)

pathFolders = app.config["UPLOAD_FOLDER"].split("/")
pathFolder = pathFolders[0]
for folder in pathFolders[1:]:
    pathFolder += "/" + folder
    if not os.path.isdir(pathFolder):
        os.mkdir(pathFolder)
        print("[INFO] Création du répertoire :", pathFolder)


SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI (without trailing '/')
API_URL = "/static/swagger.yml"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name" : "MDFilRouge"
    },
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header["Access-Control-Allow-Headers"] = '*'
    header["Access-Control-Allow-Methods"] = '*'
    return response


@app.route("/", methods=["GET"])
def index():
    return jsonify("Bienvenue sur l'API Fil Rouge !")


@app.route("/upload_file", methods=["GET", "POST"])
@login_required
def upload_file():
    """Pour extraire les métadonnées d'un fichier et les insérer dans une base
    de données, puis poster cette même image sur le système de fichiers du serveur"""

    if request.method == "POST":

        # Vérification du fichier envoyé
        file = check_request(request.files)
        if type(file) != dict:
            return file

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file['filename'])

        # Enregistrement du fichier sur le serveur
        file['file'].save(filepath)
        print("[INFO] Fichier déposé dans le répertoire {}".format(app.config['UPLOAD_FOLDER']))

        # Création de la réponse contenant les données en JSON et les métadonnées
        response = create_response(filepath)

        # Envoi dans le bucket S3
        #send_to_s3(filepath)

        # Suppression du fichier d'origine
        os.remove(filepath)
        print("[INFO] Fichier chargé par l'utilisateur supprimé du répertoire {}".format(app.config['UPLOAD_FOLDER']))
        
        # Envoi du fichier zip au client
        return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")