"""Ce module permet de récupérer les métadonnées et les données contenues dans un fichier,
d'en faire des fichiers json et de les insérer dans un fichier zip"""
# -*- coding: utf-8 -*-

import csv
import docx
import magic
import PyPDF2
from collections import Counter
from flask import abort
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS
from string import punctuation
from tinytag import TinyTag


# Dictionnaire contenant des extensions associées 
# aux MIME-type utilisés par l'API
EXT_MIME = {
    "bmp" : "image/bmp",
    "BMP" : "image/x-ms-bmp",
    "csv" : "text/csv",
    "CSV" : "application/csv",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "gif" : "image/gif",
    "jpg" : "image/jpeg",
    "jpeg": "image/jpeg",
    "png" : "image/png",
    "pdf" : "application/pdf",
    "txt" : "text/plain",
    "flac": "audio/flac",
    "Flac": "audio/x-flac",
    "fLac": "audio/x-ogg",
    "m4a" : "audio/mp4",
    "m4A" : "audio/mp4a-latm",
    "M4a" : "audio/x-m4a",
    "M4A" : "video/mp4",
    "mp3" : "audio/mpeg",
    "mP3" : "audio/MPA",
    "MP3" : "audio/mp3",
    "Mp3" : "audio/mpeg3",
    "waV" : "audio/wave",
    "wAv" : "audio/wav",
    "wav" : "audio/x-wav",
    "Wav" : "audio/vnd.wave",
    "WAV" : "audio/x-pn-wav",
    "wma" : "audio/x-ms-wma",
    "Wma" : "video/x-ms-asf",
    "opus": "audio/ogg",
    "ogg" : "audio/ogg"
}

ALLOWED_FORMATS = list(set([ext.lower() for ext in EXT_MIME.keys()]))
ALLOWED_MIME_TYPES = list(EXT_MIME.values())

def mimetype(filepath):
    """Fonction qui retourne le MIME-type d'un fichier"""

    try:
        mimeType = magic.from_file(filepath, mime=True)
        print(mimeType)
    except:
        mimeType = magic.Magic(flags=magic.flags.MAGIC_MIME_TYPE).id_filename(filepath)
        print(mimeType)
    return mimeType


def extension_from_mime(mimeType):
    """Fonction qui retourne l'extension associée au MIME-type du fichier"""

    format = None
    if mimeType in EXT_MIME.values():
        format = list(EXT_MIME.keys())[list(EXT_MIME.values()).index(mimeType)].lower()

    return format


def file_format(filepath):
    """Fonction qui récupére le format du fichier"""
    
    mimeType = mimetype(filepath)

    return extension_from_mime(mimeType)


def get_audio_metadata(filepath):
    """Fonction qui prend en entrée le chemin d'un fichier audio
    et retourne un dictionnaire contenant les métadonnées"""

    metadata = {}

    try:
        tag = TinyTag.get(filepath)

        metadata["Album"] = tag.album
        metadata["AlbumArtist"] = tag.albumartist
        metadata["Artist"] = tag.artist
        metadata["AudioOffset"] = tag.audio_offset
        metadata["Bitrate"] = tag.bitrate
        metadata["Comment"] = tag.comment
        metadata["Composer"] = tag.composer
        metadata["Disc"] = tag.disc
        metadata["DiscTotal"] = tag.disc_total
        metadata["Duration"] = tag.duration
        metadata["Genre"] = tag.genre
        metadata["Samplerate"] = tag.samplerate
        metadata["Title"] = tag.title
        metadata["Track"] = tag.track
        metadata["TrackTotal"] = tag.track_total
        metadata["Year"] = tag.year

    except:
        pass

    return metadata


def get_image_metadata(filepath):
    """Fonction qui prend en entrée le chemin d'une image et
    retourne un dictionnaire contenant les métadonnées de l'image"""

    with Image.open(filepath) as image:
        exifdata = image.getexif()

        # Création d'un dictionnaire et insertion de données
        metadata = {}
        metadata["FileName"] = image.filename.rsplit('/', 1)[1]
        metadata["Format"] = image.format

    try:
        parser = createParser(filepath)
        md = extractMetadata(parser)

        for line in md.exportPlaintext():

            # Récupération de la clé et reformatage sous la forme NameOfTheKey
            key = ''.join([w[0].upper() + w[1:] \
                for w in ''.join([x[0].upper() + x[1:] \
                    for x in line.split(':', 1)[0][2:].split(' ')]).split('-')])
            
            # Récupération de la  valeur associée
            value = line.split(':', 1)[1][1:]
            
            # Inscription dans le dictionnaire
            metadata[key] = value
            
        for tagId in exifdata:

            # Récupération des tags
            tag = TAGS.get(tagId, tagId)

            # Exclusion de certains champs
            if tag not in [
                "ComponentsConfiguration",
                "ExifImageHeight",
                "ExifImageWidth",
                "FileSource",
                "GPSInfo",
                "MakerNote",
                "PrintImageMatching",
                "SceneType"
                ] and tag.lower() not in [
                    line.split(':', 1)[0][2:].lower() 
                    for line in md.exportPlaintext()
                    ]:

                # Récupération des valeurs des tags
                data = exifdata.get(tagId)

                # Décodage des bytes
                if isinstance(data, bytes):
                    data = data.decode(errors="ignore")

                data = str(data)
                #print(f"{tag:25}:{data}")
                metadata[tag] = data

    except UnidentifiedImageError:
        abort(500, "Problème à l'ouverture de l'image. Format non pris en charge.")

    except:
        pass

    return metadata


def get_docx_metadata(filepath):
    """Fonction qui prend en entrée le chemin d'un fichier docx
    et retourne un dictionnaire contenant les métadonnées du fichier"""

    metadata = {}

    try:
        # Ouverture du fichier et récupération des informations
        doc = docx.Document(filepath)
        # Création d'un dictionnaire et insertion des différentes données
        prop = doc.core_properties
        metadata["Author"] = prop.author
        metadata["Category"] = prop.category
        metadata["Comments"] = prop.comments
        metadata["ContentStatus"] = prop.content_status
        metadata["Created"] = prop.created
        metadata["Identifier"] = prop.identifier
        metadata["KeyWords"] = prop.keywords
        metadata["Language"] = prop.language
        metadata["LastModifiedBy"] = prop.last_modified_by
        metadata["LastPrinted"] = prop.last_printed
        metadata["Modified"] = prop.modified
        metadata["Revision"] = prop.revision
        metadata["Subject"] = prop.subject
        metadata["Title"] = prop.title
        metadata["Version"] = prop.version

    except:
        pass

    return metadata


def get_pdf_metadata(filepath):
    """Fonction qui prend en entrée le chemin d'un fichier PDF
    et retourne un dictionnaire contenant les métadonnées du fichier"""

    metadata = {}

    try:
        # Ouverture du fichier et récupération des informations
        with open(filepath, 'rb') as f:
            pdf = PyPDF2.PdfFileReader(f)
            info = pdf.getDocumentInfo()
            numberOfPages = pdf.getNumPages()
        # Création d'un dictionnaire et insertion des différentes données
        metadata["Author"] = info.author
        metadata["Creator"] = info.creator
        metadata["CreationDate"] = datetime_format(info.get('/CreationDate'))
        metadata["LastModifDate"] = datetime_format(info.get('/ModDate'))
        metadata["Producer"] = info.producer
        metadata["Subject"] = info.subject
        metadata["Title"] = info.title
        metadata["NumberOfPages"] = numberOfPages

    except:
        pass

    return metadata


def get_txt_metadata(filepath):
    """Fonction qui prend en entrée le chemin d'un fichier PDF
    et retourne un dictionnaire contenant les métadonnées du fichier"""

    metadata = {}

    try:
        # Ouverture du fichier et récupération des lignes
        with open(filepath, 'r') as txtFile:
            lines = txtFile.readlines()

        wordCount = 0
        charCount = 0
        emptyLines = 0

        i = 0
        # Parcours de toutes les lines du texte
        while i < len(lines):

            # Division d'une ligne en mots
            words = lines[i].split()
            # Si la ligne est vide, ajout au compte de emptyLines
            if len(words) == 0:
                emptyLines += 1

            k = 0
            # Parcours des mots de la ligne
            while k < len(words):
                # Si le mot n'est pas composé uniquement de signes
                # de ponctuation, ajout au compte de wordCount
                iChar = 0
                while iChar < len(words[k]) and words[k][iChar] in punctuation:
                    iChar += 1
                if iChar < len(words[k]):
                    wordCount += 1
                # Ajout du nombre de caractères de chaque mot 
                # à charCount (les espaces sont exclus)
                charCount += len(words[k])
                k += 1

            i += 1

        # Contaténation des lines pour en faire 
        # un texte contenant l'intégralité des lignes
        text = "\n".join(lines)
        # Comptage des signes de ponctuation
        metadata["PunctuationMarks"] = Counter(
                char for char in text if char in punctuation)
        # Comptage des espaces
        metadata["BlankSpaces"] = Counter(
                char for char in text if char == " ")[" "]

        # Récupération des 5 mots les plus fréquents
        noPunc = ""
        for char in text:
            if char not in punctuation:
                noPunc = noPunc + char
        nbMFW = 5
        mostOccur = Counter(noPunc.split()).most_common(nbMFW)
        metadata[str(nbMFW) + "MostFrequentWords"] = {}
        for word, freq in mostOccur:
            metadata[str(nbMFW) + "MostFrequentWords"][word] = freq

        metadata["Lines"] = len(lines)
        metadata["Words"] = wordCount
        metadata["Characters"] = charCount
        metadata["EmptyLines"] = emptyLines
        metadata["MeanWordsPerLine"] = wordCount / (len(lines) - emptyLines)

    except:
        pass

    return metadata


def get_csv_metadata(filepath):
    """Fonction qui prend en entrée le chemin d'un fichier csv et
    et retourne un dictionnaire contenant les métadonnées du fichier"""

    metadata = {}

    try:
        with open(filepath, 'r', encoding='utf-8') as csvf:
            csvReader = csv.reader(csvf)

            lineCount = 0
            blankCases = 0
            for line in csvReader:
                if lineCount == 0:
                    columnNames = line
                    nbColumns = len(columnNames)
                for field in line:
                    if field == '':
                        blankCases += 1
                lineCount += 1

        metadata["BlankCases"] = blankCases
        metadata["Columns"] = nbColumns
        metadata["ColumnNames"] = columnNames
        metadata["Lines"] = lineCount

    except:
        pass

    return metadata


def datetime_format(datetime):
    """Fonction qui permet de reformater le datetime dans un format lisible"""

    if datetime == None:
        return datetime

    year = datetime[2:6]
    month = datetime[6:8]
    day = datetime[8:10]
    hours = datetime[10:12]
    minutes = datetime[12:14]
    seconds = datetime[14:16]

    return "/".join([day, month, year]) + " " + ":".join([hours, minutes, seconds])


