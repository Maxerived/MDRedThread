"""Ce module permet de vérifier les login et mot de passe dans la
base de données pour autoriser ou non l'accès à l'application"""
# -*- coding: utf-8 -*-

import hashlib
import sqlite3
from flask import abort, request
from functools import wraps


def get_hash_from_db(identifiant):

    # Connexion à la base de données
    conn = sqlite3.connect("users_auth.db")
    cur = conn.cursor()
    print("[INFO] Connexion réussie à SQLite")

    try:
        # Récupération du hash_mdp à partir de l'identifiant
        cur.execute(
            "SELECT hash_mdp FROM login_passw WHERE identifiant = ?", (identifiant,)
        )
        res = cur.fetchall()

    except sqlite3.OperationalError:
        return abort(501, "La table des utilisateurs est inexistante.")

    finally:
        # Fermeture de la base de données
        cur.close()
        conn.close()
        print("[INFO] Connexion SQlite fermée")

    if len(res) == 0:
        return None

    return res[0][0]


def login_required(f):
    """Décorateur pour vérifier que l'utilisateur est bien authentifié"""

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if request.authorization is None:
            error = "Authentification nécessaire. Ajoutez l'option -u username:password"
            abort(401, error)

        cred = request.authorization
        username = cred.get('username')
        password = cred.get('password')
        hash_db = get_hash_from_db(username)

        # Si l'identifiant n'est pas dans la base de données
        if hash_db is None:
            abort(401, "Identifiant inconnu.")

        # Récupération du salt et calcul du hash avec le salt et le mdp entré apr l'utilisateur
        salt = hash_db[:32]
        key = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, 100000, dklen=128
        )

        # Si le mot de passe est incorrect
        if hash_db[32:] != key:
            abort(401, "Mot de passe incorrect.")
    
        return f(*args, **kwargs)
    
    return decorated_function


def check_admin(password):
    """Fonction qui vérifie si les login et mot de passe sont valides"""

    hash_db = get_hash_from_db("admin")

    # Récupération du salt et calcul du hash avec le salt et le mdp entré apr l'utilisateur
    salt = hash_db[:32]
    key = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 100000, dklen=128
    )

    # Si le mot de passe est incorrect
    if hash_db[32:] != key:
        return False

    return True

