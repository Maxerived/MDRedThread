"""Ce module crée la base de données utilisateurs pour l'application flask"""
# -*- coding: utf-8 -*-

import getpass
import hashlib
import os
import sqlite3
from login import *

def create_auth_database():

    # Détermination d'un mot de passe admin au démarrage
    ADM_PSW1 = "a"
    ADM_PSW2 = "b"

    while ADM_PSW1 != ADM_PSW2:
        ADM_PSW1 = getpass.getpass("Choisissez un mot de passe admin : ")
        ADM_PSW2 = getpass.getpass("Confirmez le mot de passe admin : ")
        if ADM_PSW1 != ADM_PSW2:
            print("Les mots de passe entrés sont différents. Veuillez réessayer.")

    admin_psw = ADM_PSW1

    conn = sqlite3.connect("users_auth.db")
    cur = conn.cursor()

    # Création de la table login_passw si elle n'existe pas
    cur.execute(
        """CREATE TABLE IF NOT EXISTS login_passw
                (identifiant TEXT PRIMARY KEY,
                hash_mdp TEXT
                )"""
    )

    cur.close()
    conn.commit()
    conn.close()

    print("[INFO] Base de données créée users_auth.db avec succès.")

    insert_user("admin", admin_psw)


def insert_user(username, password):
    """Fonction qui insère un nom d'utilisateur à la base de données"""

    conn = sqlite3.connect("users_auth.db")
    cur = conn.cursor()

    # Création du hash à insérer dans la base de données pour un utilisateur lambda
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000, dklen=128)
    hash_mdp = salt + key

    # Insertion de l'utilisateur lambda
    cur.execute(
        """INSERT INTO login_passw
            (identifiant, hash_mdp) VALUES (?, ?)""",
            (username, hash_mdp)
    )

    cur.close()
    conn.commit()
    conn.close()

    print("[INFO] Utilisateur {} inséré avec succès dans la base de données.".format(username))


# Si la base de données n'existe pas
if not os.path.isfile("users_auth.db"):
    # Création de la base de données
    create_auth_database()
# Si elle n'existe pas
else:
    username = "admin"
    # Vérification de l'admin
    inputPsw = getpass.getpass("Veuillez entrer le mot de passe admin : ")
    while not check_admin(inputPsw):
        inputPsw = getpass.getpass("Veuillez entrer le mot de passe admin : ")
    # Demande si l'admin veut supprimer la base de données 
    delete = "a"
    while delete != "y" and delete != "N":
        delete = input("Voulez-vous supprimer la base de données existante ? (y/N) ")
    # S'il veut la supprimer, suppression
    if delete == "y":
        os.remove("users_auth.db")
        create_auth_database()

# Si la base de données existe déjà ou si l'admin vient de la créer ou recréer,
# demande s'il souhaite entrer un nouvel utilisateur
insert = input("Souhaitez-vous insérer un nouvel utilisateur ? (y/N) ")
while insert != "N":
    # Si l'admin souhaite ajouter un utilisateur
    if insert == "y":
        # Demande d'entrer le nom du nouvel utilisateur
        user = input("Nouvel utilisateur : ")
        PSW1 = "a"
        PSW2 = "b"
        # Demande du mot de passe associé à l'utilisateur et confirmation, 
        # tant que les deux mots de passe ne concordent pas
        while PSW1 != PSW2:
            PSW1 = getpass.getpass("Choisissez un mot de passe : ")
            PSW2 = getpass.getpass("Confirmez le mot de passe : ")
            if PSW1 != PSW2:
                print("Les mots de passe entrés sont différents. Veuillez réessayer.")
        # Si les deux mots de passe concordent, insertion du nouvel utilisateur
        psw = PSW1
        insert_user(user, psw)
    # Tant que l'admin ne répond pas par N, la question suivante est posée
    insert = input("Souhaitez-vous insérer un nouvel utilisateur ? (y/N) ")

