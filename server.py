from flask import Flask, jsonify, render_template, redirect, url_for, session, request
import threading
import subprocess
import os
import json
import requests
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from flask_session import Session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

app = Flask(__name__)
script_finalizado = False

# Configuração da sessão no Flask
app.secret_key = "chave_super_secreta"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configurações do OAuth
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid"
]

# Configuração do Cloudinary usando variáveis de ambiente
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# Função para carregar os dados da última imagem carregada do arquivo JSON
def load_image_data():
    if os.path.exists("upload_data.json"):
        with open("upload_data.json", "r") as f:
            return json.load(f)
    else:
        # Se o arquivo não existir, cria um com valores padrão
        return {"last_uploaded_image": None, "last_uploaded_time": None}

# Função para salvar os dados da imagem no arquivo JSON
def save_image_data(image_url):
    data = {"last_uploaded_image": image_url, "last_uploaded_time": str(datetime.datetime.now())}
    with open("upload_data.json", "w") as f:
        json.dump(data, f)

@app.route("/")
def home():
    image_data = load_image_data()  # Carrega os dados da imagem do JSON
    return render_template("index.html", image_url=image_data['last_uploaded_image'])

@app.route("/executar-script", methods=["POST"])
def executar_script_api():
    print("Iniciando script Selenium...")
    thread = threading.Thread(target=executar_script)
    thread.start()
    return jsonify({"message": "Script Selenium em execução..."})

@app.route("/status", methods=["GET"])
def verificar_status():
    return jsonify({"script_finalizado": script_finalizado})

# Função para upload de imagem para o Cloudinary e persistência no arquivo JSON
@app.route("/upload_imagem", methods=["POST"])
def upload_imagem():
    image_url = request.form.get("image_url")
    
    try:
        # Faz o upload da imagem para o Cloudinary
        upload_result = cloudinary.uploader.upload(image_url)
        
        # Salva a URL da imagem no arquivo JSON para persistência
        save_image_data(upload_result["secure_url"])
        
        return jsonify({"message": "Imagem carregada com sucesso!", "url": upload_result["secure_url"]})
    except Exception as e:
        return jsonify({"error": f"Erro ao fazer upload: {str(e)}"})

# Função para converter as credenciais para um formato dicionário
def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

# Dashboard após login
@app.route("/dashboard")
def dashboard():
    if "credentials" not in session:
        return redirect(url_for("login"))

    credentials = Credentials(**session["credentials"])
    response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {credentials.token}"}
    )
    user_info = response.json()
    
    return f"Olá, {user_info['name']}! Você está autenticado."

# Logout
@app.route("/logout")
def logout():
    session.pop("credentials", None)
    return redirect(url_for("login"))

# Listar arquivos do Google Drive
@app.route("/listar_arquivos")
def listar_arquivos():
    if "credentials" not in session:
        return redirect(url_for("login"))
    
    credentials = Credentials(**session["credentials"])
    drive_service = build("drive", "v3", credentials=credentials)
    
    results = drive_service.files().list(
        pageSize=10, fields="files(id, name)"
    ).execute()
    
    files = results.get("files", [])
    return jsonify({"arquivos": files})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
