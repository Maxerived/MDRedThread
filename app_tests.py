import base64
import io
import unittest

import main

TEST_PATH = "test_files/"
TEST_JPG = "test.jpg"
TEST_BMP = "test.bmp"
TEST_GIF = "test.gif"
TEST_PNG = "test.png"
TEST_PDF = "test.pdf"
TEST_DOCX = "test.docx"
TEST_CSV = "test.csv"
TEST_TXT = "test.txt"
TEST_PY = "test.py"
TEST_WF = "testpy.jpg"
TEST_MOV = "test.mov"
TEST_MP3 = "test.mp3"
TEST_FLAC = "test.flac"
TEST_M4A = "test.m4a"
TEST_OGG = "test.ogg"
TEST_OPUS = "test.opus"
TEST_WAV = "test.wav"
TEST_WMA = "test.wma"

BUCKET_NAME = "mrdv-cs"

CREDENTIALS = base64.b64encode(b'lambda:@ReTh20@').decode('utf-8')


def with_client(f):
    def func(*args, **kwargs):
        with main.app.test_client() as client:
            return f(*args, client, **kwargs)

    return func


class TestApp(unittest.TestCase):
    @with_client
    def test_upload_png(self, client):
        """Test pour une image PNG"""

        with open(TEST_PATH + TEST_PNG, "rb") as image:
            image = io.BytesIO(image.read())

        data = {"file": (image, TEST_PNG)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        json = response.get_json()
        assert response.status_code == 200
        assert len(json.keys()) == 3
        assert json["Metadata"]["FileName"] == TEST_PNG


    @with_client
    def test_upload_jpg(self, client):
        """Test pour une image JPG"""

        with open(TEST_PATH + TEST_JPG, "rb") as image:
            image = io.BytesIO(image.read())

        data = {"file": (image, TEST_JPG)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        json = response.get_json()
        assert response.status_code == 200
        assert len(json.keys()) == 3
        assert json["Metadata"]["FileName"] == TEST_JPG


    @with_client
    def test_upload_gif(self, client):
        """Test pour une image GIF"""

        with open(TEST_PATH + TEST_GIF, "rb") as image:
            image = io.BytesIO(image.read())

        data = {"file": (image, TEST_GIF)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        json = response.get_json()
        assert response.status_code == 200
        assert len(json.keys()) == 2
        assert json["Metadata"]["FileName"] == TEST_GIF


    @with_client
    def test_upload_bmp(self, client):
        """Test pour une image bmp"""

        with open(TEST_PATH + TEST_BMP, "rb") as image:
            image = io.BytesIO(image.read())

        data = {"file": (image, TEST_BMP)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        json = response.get_json()
        assert response.status_code == 200
        assert len(json.keys()) == 2
        assert json["Metadata"]["FileName"] == TEST_BMP


    @with_client
    def test_upload_pdf(self, client):
        """Test pour un fichier PDF"""

        with open(TEST_PATH + TEST_PDF, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_PDF)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        json = response.get_json()
        assert response.status_code == 200
        assert len(json.keys()) == 2
        assert json["Metadata"]["FileName"] == TEST_PDF


    @with_client
    def test_upload_docx(self, client):
        """Test pour un fichier docx"""

        with open(TEST_PATH + TEST_DOCX, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_DOCX)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        json = response.get_json()
        assert response.status_code == 200
        assert len(json.keys()) == 2
        assert json["Metadata"]["FileName"] == TEST_DOCX


    @with_client
    def test_upload_csv(self, client):
        """Test pour une image csv"""

        with open(TEST_PATH + TEST_CSV, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_CSV)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        json = response.get_json()
        assert response.status_code == 200
        assert len(json.keys()) == 2
        assert json["Metadata"]["FileName"] == TEST_CSV


    @with_client
    def test_upload_txt(self, client):
        """Test pour un fichier txt"""

        with open(TEST_PATH + TEST_TXT, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_TXT)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        json = response.get_json()
        assert response.status_code == 200
        assert len(json.keys()) == 2
        assert json["Metadata"]["FileName"] == TEST_TXT


    @with_client
    def test_upload_mp3(self, client):
        """Test pour un fichier mp3"""

        with open(TEST_PATH + TEST_MP3, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_MP3)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        json = response.get_json()
        assert response.status_code == 200
        assert len(json.keys()) == 2
        assert json["Metadata"]["FileName"] == TEST_MP3


    @with_client
    def test_upload_flac(self, client):
        """Test pour un fichier flac"""

        with open(TEST_PATH + TEST_FLAC, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_FLAC)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        json = response.get_json()
        assert response.status_code == 200
        assert len(json.keys()) == 2
        assert json["Metadata"]["FileName"] == TEST_FLAC


    @with_client
    def test_upload_m4a(self, client):
        """Test pour un fichier m4a"""

        with open(TEST_PATH + TEST_M4A, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_M4A)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        json = response.get_json()
        assert response.status_code == 200
        assert len(json.keys()) == 2
        assert json["Metadata"]["FileName"] == TEST_M4A


    @with_client
    def test_upload_ogg(self, client):
        """Test pour un fichier ogg"""

        with open(TEST_PATH + TEST_OGG, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_OGG)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        json = response.get_json()
        assert response.status_code == 200
        assert len(json.keys()) == 2
        assert json["Metadata"]["FileName"] == TEST_OGG


    @with_client
    def test_upload_opus(self, client):
        """Test pour un fichier opus"""

        with open(TEST_PATH + TEST_OPUS, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_OPUS)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        json = response.get_json()
        assert response.status_code == 200
        assert len(json.keys()) == 2
        assert json["Metadata"]["FileName"] == TEST_OPUS


    @with_client
    def test_upload_wav(self, client):
        """Test pour un fichier wav"""

        with open(TEST_PATH + TEST_WAV, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_WAV)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        json = response.get_json()
        assert response.status_code == 200
        assert len(json.keys()) == 2
        assert json["Metadata"]["FileName"] == TEST_WAV


    @with_client
    def test_upload_wma(self, client):
        """Test pour un fichier wma"""

        with open(TEST_PATH + TEST_WMA, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_WMA)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        json = response.get_json()
        assert response.status_code == 200
        assert len(json.keys()) == 2
        assert json["Metadata"]["FileName"] == TEST_WMA


    @with_client
    def test_upload_too_big_file(self, client):
        """Test pour un fichier trop volumineux"""

        with open(TEST_PATH + TEST_MOV, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_MOV)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        assert response.status_code == 413


    @with_client
    def test_upload_wrong_extension(self, client):
        """Test pour un fichier dont l'extension est invalide"""

        with open(TEST_PATH + TEST_PY, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_PY)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        assert response.status_code == 415
        assert "Extension inexistante ou non prise en charge." in response.data.decode('utf-8')


    @with_client
    def test_upload_wrong_format(self, client):
        """Test pour un fichier dans un format non pris en charge par l'API"""

        with open(TEST_PATH + TEST_WF, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_WF)}

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            data=data,
            content_type="multipart/form-data"
            )

        assert response.status_code == 415
        assert "Extensions acceptées" in response.data.decode('utf-8')


    @with_client
    def test_without_auth(self, client):
        """Test sans authentification"""

        with open(TEST_PATH + TEST_PDF, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_PDF)}

        response = client.post("/upload",
            data=data,
            content_type="multipart/form-data"
            )

        assert response.status_code == 401
        assert "Authentification nécessaire." in response.data.decode('utf-8')


    @with_client
    def test_wrong_login(self, client):
        """Test avec un login inexistant en base de données utilisateurs"""

        with open(TEST_PATH + TEST_PDF, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_PDF)}
        wrongCred = base64.b64encode(b'WrongLogin:@ReTh20@').decode('utf-8')

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {wrongCred}'},
            data=data,
            content_type="multipart/form-data"
            )

        assert response.status_code == 401
        assert "Identifiant inconnu." in response.data.decode('utf-8')


    @with_client
    def test_wrong_password(self, client):
        """Test avec un mot de passe incorrect"""

        with open(TEST_PATH + TEST_PDF, "rb") as file:
            file = io.BytesIO(file.read())

        data = {"file": (file, TEST_PDF)}
        wrongCred = base64.b64encode(b'lambda:WrongPswd').decode('utf-8')

        response = client.post("/upload",
            headers={"Authorization" : f'Basic {wrongCred}'},
            data=data,
            content_type="multipart/form-data"
            )

        assert response.status_code == 401
        assert "Mot de passe incorrect." in response.data.decode('utf-8')


    @with_client
    def test_list_files(self, client):
        """Test de récupération du nom des fichiers dans le bucket"""

        response = client.get("/list_files",
            headers={"Authorization" : f'Basic {CREDENTIALS}'},
            content_type="multipart/form-data"
            )

        assert response.status_code == 200
        assert type(response.get_json()) is dict

