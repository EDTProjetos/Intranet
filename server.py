from flask import Flask, jsonify, render_template, redirect, url_for, session, request
import threading
import subprocess
import os
import json
import requests
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

def executar_script():
    """Executa o script Selenium"""
    global script_finalizado
    script_finalizado = False
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(BASE_DIR, "gerar_perfil_aut.py")
    
    if os.path.exists(script_path):
        try:
            print(f"Executando script em: {script_path}")
            result = subprocess.run(
                ["python3", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"Saída do script: {result.stdout}")
            print(f"Erros do script: {result.stderr}")
            script_finalizado = result.returncode == 0
            if script_finalizado:
                print("Script executado com sucesso!")
            else:
                print(f"Erro ao executar o script: {result.stderr}")
        except Exception as e:
            print(f"Erro ao executar script: {str(e)}")
            script_finalizado = False
    else:
        print(f"O script não foi encontrado no caminho: {script_path}")
        script_finalizado = False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/executar-script", methods=["POST"])
def executar_script_api():
    print("Iniciando script Selenium...")
    thread = threading.Thread(target=executar_script)
    thread.start()
    return jsonify({"message": "Script Selenium em execução..."})

@app.route("/status", methods=["GET"])
def verificar_status():
    return jsonify({"script_finalizado": script_finalizado})

# Rota para login com Google
@app.route("/login")
def login():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": [GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
    )
    
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    
    session["state"] = state
    return redirect(authorization_url)

# Callback do Google OAuth
@app.route("/auth/callback")
def auth_callback():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": [GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        state=session["state"],
    )
    
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session["credentials"] = credentials_to_dict(credentials)
    
    return redirect(url_for("dashboard"))

# Converter credenciais para dicionário
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
