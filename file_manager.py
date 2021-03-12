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
from functools import wraps


ALLOWED_FORMATS = ["bmp", "csv", "docx", "gif", "jpg", "jpeg", "pdf", "png", "txt"]
ALLOWED_IMAGE_FORMATS = ["bmp", "gif", "jpg", "jpeg", "png"]
BUCKET_NAME = "mdrv-cs"
TEMP_FOLDER="./static/temp"


def empty_temp_folder(f):
    """Décorateur pour vider le répertoire /static/temp"""

    @wraps(f)
    def decorated_function(*args, **kwargs):

        for file in os.listdir(TEMP_FOLDER):
            os.remove(os.path.join(TEMP_FOLDER, file))
    
        return f(*args, **kwargs)

    return decorated_function


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

        bucketObjects = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        if 'Contents' in bucketObjects:

            # Récupération de la liste des noms des objets contenus dans le bucket s3
            bucketObjectsList = [obj.get('Key') \
                for obj in bucketObjects.get('Contents')]
                        
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
        abort(401, "Credentials invalides !")
    except ProfileNotFound:
        abort(401, "Profil AWS non trouvé")
    except:
        abort(500, "Un problème est survenu lors du chargement dans le bucket s3.")


def list_files_in_bucket():
    """Fonction qui renvoie le nom des fichiers insérés dans le bucket S3"""

    try:
        # Connexion à s3 avec les credentials
        session = boto3.Session(profile_name = 'csloginstudent')
        s3_client = session.client('s3')
        
        bucketObjects = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        files = {}

        if 'Contents' in bucketObjects:

            # Récupération de la liste des noms des objets contenus dans le bucket s3
            bucketObjectsList = [obj.get('Key') \
                for obj in bucketObjects.get('Contents')]

            # Tranformation de la liste en dictionnaire (pour jsonify)
            i = 0
            while i < len(bucketObjectsList):
                files["file" + "{:04d}".format(i + 1)] = bucketObjectsList[i]
                i += 1

        return files

    except NoCredentialsError:
        abort(401, "Credentials invalides !")
    except ProfileNotFound:
        abort(401, "Profil AWS non trouvé")
    except:
        abort(500, "un problème non géré est survenu.")


def download_from_bucket(filename):
    """Fonction qui renvoie le nom des fichiers insérés dans le bucket S3"""

    try:
        # Connexion à s3 avec les credentials
        session = boto3.Session(profile_name = 'csloginstudent')
        s3_client = session.client('s3')

        bucketObjects = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        if 'Contents' in bucketObjects:
            
            # Récupération de la liste des noms des objets contenus dans le bucket s3
            bucketObjectsList = [obj.get('Key') \
                for obj in bucketObjects.get('Contents')]

            if filename in bucketObjectsList:
                s3_client.download_file(
                    BUCKET_NAME,
                    filename,
                    os.path.join(TEMP_FOLDER, filename)
                )

    except NoCredentialsError:
        abort(401, "Credentials invalides !")
    except ProfileNotFound:
        abort(401, "Profil AWS non trouvé")
    except:
        abort(500, "Un problème non géré est survenu.")


def delete_all_bucket_files():
    """Fonction supprime tous les fichiers déposés
    dans le bucket S3 par les utilisateurs"""

    try:
        # Connexion à s3 avec les credentials
        session = boto3.Session(profile_name = 'csloginstudent')
        s3_client = session.client('s3')

        bucketObjects = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        if 'Contents' in bucketObjects:
            for item in bucketObjects['Contents']:
                print('[INFO] Deleting file', item['Key'])
                s3_client.delete_object(Bucket=BUCKET_NAME, Key=item['Key'])
                while bucketObjects['KeyCount'] == 1000:
                     bucketObjects = s3_client.list_objects_v2(
                         Bucket=BUCKET_NAME,
                         StartAfter=bucketObjects['Contents'][0]['Key'],
                     )
                for item in bucketObjects['Contents']:
                    print('[INFO] Deleting file', item['Key'])
                    s3_client.delete_object(Bucket=BUCKET_NAME, Key=item['Key'])

    except NoCredentialsError:
        abort(401, "Credentials invalides !")
    except ProfileNotFound:
        abort(401, "Profil AWS non trouvé")
    except:
        abort(500, "Un problème non géré est survenu.")


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

