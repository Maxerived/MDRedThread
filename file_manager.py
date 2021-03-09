"""Module qui permet de créer les fichiers utiles et d'envoyer sur le bucket s3"""
# -*- coding: utf-8 -*-

import base64
import boto3
import json
import logging
import os
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound
from datetime import datetime
from flask import abort
from get_metadata import *
from werkzeug.utils import secure_filename


ALLOWED_FORMATS = ["bmp", "csv", "docx", "gif", "jpg", "jpeg", "pdf", "png", "txt"]
ALLOWED_IMAGE_FORMATS = ["bmp", "gif", "jpg", "jpeg", "png"]
BUCKET_NAME = "mdrv-cs"
ZIP_FILENAME = "json_temp.zip"    


def get_metadata(filepath):
    """Fonction qui récupère les métadonnées du fichier passé en paramètre"""

    mimeType = mimetype(filepath)
    format = extension_from_mime(mimeType)
    #print("Format du fichier :", format)

    metadata = {}

    # Si le format n'est pas pris en charge par l'application
    if format not in ALLOWED_FORMATS:
        abort(415, "Formats acceptés : " + str(ALLOWED_FORMATS))

    # Si le fichier est une image
    if format in ALLOWED_IMAGE_FORMATS:
        # Récupération des métadonnées
        metadata = get_image_metadata(filepath)

    # Si le fichier est un .docx
    if format == "docx":
        # Récupération des métadonnées
        metadata = get_docx_metadata(filepath)

    # Si le fichier est un PDF
    if format == "pdf":
        # Récupération des métadonnées
        metadata = get_pdf_metadata(filepath)

    # Si le fichier est un .txt
    if format == "txt":
        # Récupération des métadonnées
        metadata = get_txt_metadata(filepath)

    # Si le fichier est un .csv
    if format.lower() == "csv":
        metadata = get_csv_metadata(filepath)

    # Ajout d'autres éléments de métadonnées
    metadata["FileName"] = filepath.rsplit('/', 1)[1]
    metadata["FileSize"] = str(os.stat(filepath).st_size / 1000000) + " Mo"
    if format not in {"bmp", "png", "jpg", "jpeg"}:
        metadata["MimeType"] = mimeType

    return metadata


def jsonify_data(filepath):
    """Fonction qui récupère les métadonnées du fichier passé en paramètre"""

    format = file_format(filepath)
    #print("Format du fichier :", format)

    data = {}

    # Si le format n'est pas pris en charge par l'application
    if format == None or format.lower() not in ALLOWED_FORMATS:
        abort(415, "Formats acceptés : " + str(ALLOWED_FORMATS))

    # Si le fichier est une image
    if format in ALLOWED_IMAGE_FORMATS + ["docx", "pdf"]:
        # Récupération des données et encodage en base64
        with open(filepath, mode='rb') as file:
            data = base64.b64encode(file.read()).decode('utf-8')

    # Si le fichier est un .txt
    if format in ["txt", "csv"]:
        # Récupération des données
        with open(filepath, 'r') as file:
            data = file.read()

    return json.dumps(data)


def send_to_s3(filepath):
    """Fonction qui envoie un fichier dans le bucket S3 défini dans l'API"""

    filename = datetime.strftime(datetime.now(), "%F_%H-%M-%S_") + filepath.rsplit('/', 1)[-1]

    try:
        # Connexion à s3 avec les credentials
        session = boto3.Session(profile_name = 'csloginstudent')
        s3_client = session.client('s3')
        
        # Récupération de la liste des noms des objets contenus dans le bucket s3
        bucketObjectsList = [obj.get('Key') \
            for obj in s3_client.list_objetcs(Bucket=BUCKET_NAME).get('Contents')]
        
        # Changement de filename si un objet a déjà le nom défini
        index = 1
        while filename in bucketObjectsList:
            index += 1
            filename += "_" + str(index)

        # Chargement du fichier dans le bucket s3
        s3_client.upload_file(Filename = filepath, Bucket = BUCKET_NAME, Key = filename)
        print("[INFO] Fichier charge avec succes dans le bucket S3.")

    except ClientError as e:
        logging.error(e)
        abort(500, "Problème lors du chargement du fichier vers le bucket S3.")

    except NoCredentialsError:
        abort(500, "Credentials invalides !")

    except ProfileNotFound:
        abort(500, "Profil AWS non trouvé")

    except:
        abort(500, "Un problème est survenu lors du chargement dans le bucket s3.")


def image_reko(filepath, nbLabels):
    """Fonction qui fait appel a rekognition (AWS) pour détecter
    les ojets reconnus dans l'image"""

    try:
        session = boto3.Session(profile_name = 'csloginstudent')
        reko_client = session.client('rekognition')

        with open(filepath, 'rb') as image:
            response = reko_client.detect_labels(Image={'Bytes': image.read()}, MaxLabels=nbLabels)
        
        # Récupération de la liste des labels
        labels = {}
        for label in response['Labels']:
            labels[label['Name']] = round(label['Confidence'], 2)

    except ProfileNotFound:
        labels = None

    except:
        abort(500, "Un problème est survenu lors de la requête à rekognition.")

    return labels


def good_extension(filename):
    """Fonction qui vérifie si l'extension du fichier est
    parmi les formats pris en charge par l'application"""

    # Récupération de l'extension du fichier
    extension = filename.rsplit(".", 1)[-1].lower()
    allowedFile = "." in filename and extension in ALLOWED_FORMATS

    return allowedFile


def check_request(requestFile):
    """Fonction qui prend en entrée un dictionnaire comprenant un nom de fichier
    et le contenu associé, vérifie s'il y a bien un fichier dans la requête
    et retourne un dictionnaire comprenant le nom sécurisé du fichier
    et le contenu du fichier, ou un message d'erreur"""

    # Vérification de la validité du fichier
    if "file" not in requestFile:
        abort(500, "Fichier vide")

    # Récupération du fichier de la requête
    file = requestFile["file"]

    # Vérification qu'un fichier est sélectionné
    if file.filename == "":
        abort(500, "Aucun fichier sélectionné")

    filename = file.filename
    secFilename = secure_filename(filename)

    if not good_extension(filename):
        abort(415, "Extension inexistante ou non prise en charge.")

    return {'filename' : secFilename, 'file' : file}


def create_response(filepath):
    """Fonction qui crée la réponse à retourner au client"""

    response = {
                'DataInJson' : jsonify_data(filepath),
                'Metadata' : get_metadata(filepath)
            }

    format = file_format(filepath)
    #print("Format du fichier :", format)
    
    if format.lower() in ["jpeg", "jpg", "png"]:
        detected = image_reko(filepath, 20)
        if detected is not None:
            response['Recognized'] = detected

    return response

