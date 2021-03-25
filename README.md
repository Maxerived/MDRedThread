#### Projet MDRedThread

Implémentée en python3 et avec Flask comme moteur web, l’API développée prend en charge les fichiers dont le format est parmi les suivants : txt, csv, docx, pdf, bmp, gif, jpg, png, flac, mp3, ogg, wav, wma, m4a, opus.

Pour fonctionner, l’application s’appuie sur les fichiers suivants :
- main.py : on y retrouve toutes les routes qui permettent d’accéder aux différentes fonctionnalités ;
- file_manager.py : ce module contient toutes les fonctions qui permettent de faire les traitements nécessaires sur les fichiers soumis par l’utilisateur ;
- get_metadata.py : ce module contient les fonctions qui permettent de récupérer les métadonnées des fichiers soumis en fonction du type de fichier ;
- login.py : ce module contient des fonctions et décorateurs qui permettent l’authentification de l’utilisateur et donc l’accès à l’application ;
- users_auth.db : cette base de données est celle sur laquelle s’appuie l’application pour l’authentification des utilisateurs.


### Installation de l'API

Dans un premier temps, récupérez tout le contenu du présent répertoire et placez vous dedans.

Ensuite, depuis votre terminal, lancez la commande suivante pour installer tous les packages nécessaires à la bonne utilsation de l'API :
```
pip3 install requirements.txt
```
Exécutez la commande suivante pour initialiser la base de données qui servira à l'authentification et donc à la connexion à l'API :
```
python3 users_db.py
```
Vous devrez définir un mot de passe administrateur et vous ensuite la possibilité d'ajouter d'autres utilisateurs.

## Lancement de l'API en local

Il vous suffit maintenant d'exécuter la commande suivante pour lancer l'API sur votre serveur local :
```
FLASK_APP=main.py flask run
```
Si vous voulez déployer l'API dans un environnement de développement, il peut être intéressant d'exécuter cette commande : ```FLASK_APP=main.py FLASK_ENV=development flask run --reload```

## Lancement de l'API sur un serveur en utilisant docker-compose et ngninx pour du loadbalancing

Après avoir installé docker-compose, exécutez la commande suivante :
```
docker-compose up --build --scale flask=3
```
Cette commande vous permettra de déployer 3 conteneurs pour votre application. Vous pouvez aller jusqu'à 5. Nota : en fonction du serveur sur lequel vous déployez et les droits que vous avez, la commande devra peut-être être précédée de sudo.


### Utilisation de l'API

## Authentification

Pour accéder aux différents services proposés par l’application, une authentification est nécessaire. Elle est mise en œuvre grâce à une petite base de données contenant une table à deux colonnes (identifiant, hash_mdp). Le script python users_db.py permet de :
- créer la base de données si elle n’existe pas,
- la supprimer si elle existe, après s’être authentifié en tant qu’admin (limite : il est possible de supprimer facilement la base de données grâce à la commande shell rm),
- rajouter de nouveaux utilisateurs dans la base de données,
- supprimer des utilisateurs de la base (pour faciliter cette manipulation, la liste des utilisateurs s’affiche si l’admin choisit de supprimer un utilisateur).

Ainsi, lorsqu’une requête est soumise à l’application, un décorateur python pour authentifier l’utilisateur autorise ou non l’accès et la poursuite du processus. Si aucun élément d’authentification n’est envoyé, si l’utilisateur n’est pas dans la base de données ou si le mot de passe est incorrect, le retour de l’API est une erreur 401, accompagnée d’un message indiquant la nature du problème. Dans le cas contraire, le processus peut alors se poursuivre.

Actuellement, les mots de passe sont transmis en clair à l’application. Une amélioration consisterait à les faire transiter de manière secrète

# Commandes

La base de la commande permettant d’accéder aux différents services de l’application est la suivante :

curl -kiL -X <METHOD> -u <username:password> https://url_serveur/

L’option -L est utile dans le cas où l’utilisateur tape sa requête en http. Cela va permettre d’obtenir le résultat après redirection sur le port 443 en https.

Il est possible de n’indiquer que le username lorsque vous faites la requête, ce qui est recommandé pour des questions de sécurité. Il est ensuite demandé le mot de passe, qui ne s’affichera pas à l’écran.
Le fichier de tests intitulé tests.sh permet de tester l’API avec un fichier de chaque type que l’application est censée prendre en charge. Pour les fichiers un peu volumineux, il faut s’attendre à des délais de réponse un peu longs.
Si l'API est déployée dans des conteneurs avec docker-compose et nginx, la limite du nombre de requêtes est fixée à 12r/min. Si celle-ci est dépassée, le retour indique une indisponibilité temporaire du service.


# Fonctionnalités

Les fonctionnalités développées sont les suivantes : index, upload, list_files, download, empty_bucket.

* index

Cette fonctionnalité n’est autre que la page d’accueil de l’API. On ne peut plus simple dans sa forme, elle n’a eu d’intérêt que pour tester l’application, sans authentification. Tout le monde peut donc y accéder.

curl -kiL -X GET https://url_serveur/

* upload

Cette fonctionnalité est celle imposée par l’exercice. La requête qui permet d’accéder à celle-ci est la suivante :

curl -kiL -X POST -u <username:password> https://url_serveur/upload -F "file=@<path/of/the/file.ext>"

Après authentification, le nom du fichier est sécurisé puis il est vérifié que le fichier ait une extension et que celle-ci soit acceptée par l’application. Ensuite le fichier est enregistré temporairement dans le dossier static/temp.

Après cette première étape, une vérification du mime-type du fichier est opérée. Celui-ci est converti en une extension d’après un dictionnaire dont les clés sont les extensions et les valeurs les mime-types. Si l’extension obtenue fait partie des extensions acceptées, alors le processus se poursuit. Dans le cas contraire, le message d’erreur est renvoyé à l’utilisateur.

Ensuite, si le fichier est un .csv ou un .txt, le contenu de celui-ci est directement converti au format JSON. Dans le cas des fichiers binaires, ceux-ci sont encodés en base64 avant d’être jsonifiés. L’élément généré est inséré dans un dictionnaire avec pour clé l’intitulé DataInJson. Parallèlement, les métadonnées du fichier sont récupérées en fonction de son format et insérées dans le même dictionnaire avec pour clé l’intitulé naturel Metadata. Enfin, si le fichier est au format .jpg ou .png, après vérification des credentials AWS, celui-ci est soumis à Amazon Rekognition pour relever les éléments reconnus dans l’image, dans la limite de 20, accompagnés du taux de fiabilité en %. Ces éléments sont insérés dans le dictionnaire avec pour clé l’intitulé Recognized.

Après que ce dictionnaire a été construit, une nouvelle vérification des credentials est réalisée et le fichier est envoyé sur le bucket S3 avec un nom de fichier qui reprend le nom de fichier initial et le fait précéder de la date et l’heure de dépôt. S’il existe déjà un fichier du même nom, un chiffre est ajouté entre le nouveau nom du fichier et son extension.

Pour terminer, le fichier ayant enregistré temporairement sur le serveur et étant archivé dans le bucket S3, il est supprimé du répertoire static/temp et le dictionnaire généré pendant tout le processus est renvoyé à l’utilisateur.

L’enregistrement du fichier sur le serveur a cet avantage qu’il est ensuite possible d’accéder à celui-ci autant de fois que l’on en a besoin jusqu’à la fin de son traitement et sa suppression en fin de processus.

* list_files

Cette fonctionnalité permet de lister tous les fichiers déposés dans le bucket S3. Elle est utilisable par tous les utilisateurs enregistrés dans la base de données utilisateurs. La commande est la suivante :

curl -kiL -X GET -u <username:password> https://url_serveur/list_files

* download

Cette fonctionnalité permet de télécharger un fichier se trouvant dans le bucket S3. Elle est utilisable par tous les utilisateurs enregistrés dans la base de données utilisateurs. La commande est la suivante :

curl -kiL -X GET -u <username:password> https://url_serveur/download/<filename> (--output <destinationfilepath>)

Dans le processus, le serveur télécharge dans un premier temps le fichier demandé depuis le bucket S3 dans son répertoire static/temp. C’est ce fichier qui est ensuite envoyé depuis le serveur à l’utilisateur avec Flask. Les fichiers .txt et .csv vont s’afficher directement dans terminal de l’utilisateur. Les fichiers binaires, quant à eux, vont devoir être enregistrés dans un fichier via l’option --output indiqué dans la commande ci-dessus.

Pour éviter que les fichiers téléchargés ne s’accumulent dans le répertoire static/temp et qu’ils génèrent des conflits potentiels par la suite, le fichier enregistré temporairement à chaque requête est supprimé après l’envoi à l’utilisateur.

* empty_bucket

Cette fonctionnalité permet de supprimer tous les fichiers se trouvant dans le bucket S3. Elle est accessible uniquement à l’administrateur. Pour que celle-ci soit réalisable, le droit d’accès à été accordé à M. François Laissus, Cyril Rognon et Aurélien Joga, avec leur login et mot de passe respectif. La commande est la suivante :

curl -kiL -X DELETE -u admin https://url_serveur/empty_bucket
