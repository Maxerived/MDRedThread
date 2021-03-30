#!/bin/bash

echo "|-----------------------------------------------------------------------------|"
echo "|                                     TESTS                                   |"
echo "|-----------------------------------------------------------------------------|"
echo ""
echo "Bonjour et bienvenue pour les tests de l'API !"
echo ""
echo "Vous vous apprêtez à débuter les tests de l'application."
echo "Je vous rappelle que la limite du nombre de requêtes est paramétrée"
echo "à 12 par minutes. Si vous allez trop vite, vous aurez peut-être droit"
echo "à une indisponibilité temporaire du service."
echo ""
read -p "Entrez votre nom d'utilisateur: " username
read -s -p "Entrez votre mot de passe : " password
echo ""
echo "|-----------------------------------------------------------------------------|"
echo "|              Test de l'API pour accéder à la page d'accueil                 |"
echo "|-----------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X GET https://redthreadapi.drv.p2021.ajoga.fr/"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X GET https://redthreadapi.drv.p2021.ajoga.fr/
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|-----------------------------------------------------------------------------|"
echo "|                   Test de l'API en envoyant un fichier PNG                  |"
echo "|-----------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.png'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.png"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|-----------------------------------------------------------------------------|"
echo "|                   Test de l'API en envoyant un fichier JPG                  |"
echo "|-----------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.jpg'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.jpg"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|-----------------------------------------------------------------------------|"
echo "|                   Test de l'API en envoyant un fichier BMP                  |"
echo "|-----------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.bmp'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.bmp"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|-----------------------------------------------------------------------------|"
echo "|                   Test de l'API en envoyant un fichier GIF                  |"
echo "|-----------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.gif'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.gif"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|                   Test de l'API en envoyant un fichier CSV                   |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.csv'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.csv"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|                   Test de l'API en envoyant un fichier TXT                   |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.txt'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.txt"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|                   Test de l'API en envoyant un fichier DOCX                  |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo "curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.docx'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.docx"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|                   Test de l'API en envoyant un fichier PDF                   |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.pdf'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.pdf"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|                   Test de l'API en envoyant un fichier MP3                   |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.mp3'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.mp3"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|                   Test de l'API en envoyant un fichier M4A                   |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.m4a'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.m4a"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|                   Test de l'API en envoyant un fichier FLAC                  |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.flac'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.flac"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|                   Test de l'API en envoyant un fichier OGG                   |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.ogg'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.ogg"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|                   Test de l'API en envoyant un fichier OPUS                  |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.opus'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.opus"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|                   Test de l'API en envoyant un fichier WAV                   |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.wav'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.wav"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|                   Test de l'API en envoyant un fichier WMA                   |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.wma'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.wma"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|  Test de l'API en envoyant un fichier avec une extension non prise en charge |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.py'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.py"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|    Test de l'API en envoyant un fichier dans un format non pris en charge    |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/testpy.jpg'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/testpy.jpg"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|             Test de l'API en envoyant un fichier trop volumineux             |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.mov'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.mov"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|                   Test de l'API sans authentification                        |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.txt'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.txt"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|                    Test de l'API avec un login inconnu                       |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u WrongLogin:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.txt'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u WrongLogin:$password https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.txt"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|                 Test de l'API avec un mot de passe invalide                  |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:WrongPassword https://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.txt'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:WrongPassword https://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.txt"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|                  Test de l'API en faisant une requête http                   |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X POST -u $username:<yourpswd> http://redthreadapi.drv.p2021.ajoga.fr/upload -F 'file=@test_files/test.txt'"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X POST -u $username:$password http://redthreadapi.drv.p2021.ajoga.fr/upload -F "file=@test_files/test.txt"
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|            Test de l'API pour lister les fichiers dans le bucket             |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X GET -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/list_files"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X GET -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/list_files
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|          Test de l'API pour télécharger un fichier depuis le bucket          |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X GET -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/download/<filename>"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "Il va vous être demandé de copier-coller l'un des noms de fichier listés"
echo "ci-dessus. Les fichiers txt et csv s'afficheront directement en réponse."
echo "La réponse avec les fichiers dans les autres formats vous suggéreront d'ajouter"
echo "une option supplémentaire pour enregistrer le fichier."
read -p "Copiez-collez ici le nom d'un des fichiers listés ci-dessus : " file
curl -kiL -X GET -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/download/$file
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|            Test de l'API pour effacer tous les fichiers du bucket            |"
echo "|               (seul l'administrateur le peut en temps normal)                |"
echo "|------------------------------------------------------------------------------|"
echo ""
echo "Requête exécutée :"
echo """curl -kiL -X DELETE -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/empty_bucket"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X DELETE -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/empty_bucket
echo ""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
echo "|------------------------------------------------------------------------------|"
echo "|            Test de l'API pour vérifier que le bucket bien vide               |"
echo "|------------------------------------------------------------------------------|"
echo "Requête exécutée :"
echo """curl -kiL -X GET -u $username:<yourpswd> https://redthreadapi.drv.p2021.ajoga.fr/list_files"""
read -n 1 -r -s -p $'Appuyez sur Entrée pour continuer\n'
curl -kiL -X GET -u $username:$password https://redthreadapi.drv.p2021.ajoga.fr/list_files
echo ""
echo "Les tests sont terminés !!"
echo ""
