"""Ce module permet d'accéder à proprement parler à l'application se trouvant sur le serveur"""
# -*- coding: utf-8 -*-

import os

from flask import abort, Flask, jsonify, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from file_manager import *
from login import *


app = Flask(__name__)

app.config['TEMP_FOLDER'] = "./static/temp"
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024
app.secret_key = os.urandom(24)

PATH_FOLDERS = app.config["TEMP_FOLDER"].split("/")
pathFolder = PATH_FOLDERS[0]
for folder in PATH_FOLDERS[1:]:
    pathFolder += "/" + folder
    if not os.path.isdir(pathFolder):
        os.mkdir(pathFolder)
        print("[INFO] Création du répertoire :", pathFolder)


SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI (without trailing '/')
API_URL = "/static/swagger.yaml"

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name" : "MDFilRouge"
    },
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header["Access-Control-Allow-Headers"] = '*'
    header["Access-Control-Allow-Methods"] = '*'
    return response


@app.route("/", methods=["GET"])
def index():
    """Page d'accueil de l'API"""

    return jsonify("Bienvenue sur l'API Fil Rouge !"), 200


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    """Pour extraire les métadonnées d'un fichier et les insérer dans une base
    de données, puis poster cette même image sur le système de fichiers du serveur"""

    if request.method == "POST":

        # Vérification du fichier envoyé
        file = check_request(request.files)

        filepath = os.path.join(app.config['TEMP_FOLDER'], file['filename'])

        # Enregistrement du fichier sur le serveur
        file['file'].save(filepath)
        print("[INFO] Fichier déposé dans le répertoire {}".format(app.config['TEMP_FOLDER']))

        # Création de la réponse contenant les données en JSON et les métadonnées
        response = create_response(filepath)

        # Envoi dans le bucket S3
        send_to_s3(filepath)

        # Suppression du fichier d'origine
        os.remove(filepath)
        print("[INFO] Fichier chargé par l'utilisateur supprimé du répertoire {}".format(
            app.config['TEMP_FOLDER']))

        return response, 200


@app.route("/list_files", methods=["GET"])
@login_required
def list_files():
    """Fonction qui renvoie le nom de tous les fichiers dans le bucket S3"""

    return jsonify(list_files_in_bucket()), 200


@app.route("/download/<filename>", methods=["GET", "POST"])
@login_required
def download(filename):
    """Fonction qui télécharge un fichier depuis le bucket S3"""

    download_from_bucket(filename)

    if os.path.isfile(os.path.join(app.config['TEMP_FOLDER'], filename)):
        try:
            return send_from_directory(app.config['TEMP_FOLDER'], filename, as_attachment=True), 200
        finally:
            if os.path.isfile(os.path.join(app.config['TEMP_FOLDER'], filename)):
                os.remove(os.path.join(app.config['TEMP_FOLDER'], filename))

    else:
        return '', 204


@app.route("/empty_bucket", methods=["DELETE"])
@admin_required
def empty_bucket():
    """Fonction qui supprime tous les objets du bucket"""

    delete_all_bucket_files()

    return jsonify("Tous les fichiers du bucket S3 ont ete supprimes."), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
