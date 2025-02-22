from flask import Flask, jsonify, render_template, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
import threading
import subprocess
import os
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
import googleapiclient.discovery

app = Flask(__name__)
app.secret_key = os.environ.get("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")

# Configuração do OAuth do Google
app.config['GOOGLE_CLIENT_ID'] = os.environ.get("GOOGLE_CLIENT_ID")
app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get("GOOGLE_CLIENT_SECRET")
app.config['GOOGLE_DISCOVERY_URL'] = "https://accounts.google.com/.well-known/openid-configuration"

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
    client_kwargs={'scope': 'openid email profile https://www.googleapis.com/auth/drive'},
)

script_finalizado = False

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

# --- Rotas de OAuth do Google ---
@app.route("/login")
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/authorize")
def authorize():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    session['user'] = user_info

    # Salvar as credenciais do Google Drive
    credentials = token
    session['credentials'] = credentials

    return redirect(url_for('home'))

@app.route("/logout")
def logout():
    session.pop('user', None)
    session.pop('credentials', None)
    return redirect(url_for('home'))

@app.route("/userinfo")
def userinfo():
    user = session.get('user')
    if user:
        return jsonify(user)
    return jsonify({"error": "not logged in"}), 401

# --- Funções para interação com Google Drive ---

def get_drive_service():
    """Obtém o serviço do Google Drive com base nas credenciais"""
    credentials = session.get('credentials')
    if credentials:
        creds = Credentials.from_authorized_user_info(credentials)
        return googleapiclient.discovery.build('drive', 'v3', credentials=creds)
    return None

@app.route("/drive/files", methods=["GET"])
def list_files():
    """Lista arquivos no Google Drive do usuário"""
    drive_service = get_drive_service()
    if not drive_service:
        return jsonify({"error": "não autorizado"}), 401

    results = drive_service.files().list(pageSize=10, fields="files(id, name)").execute()
    files = results.get('files', [])
    return jsonify({"files": files})

@app.route("/drive/upload", methods=["POST"])
def upload_file():
    """Faz upload de um arquivo para o Google Drive"""
    drive_service = get_drive_service()
    if not drive_service:
        return jsonify({"error": "não autorizado"}), 401

    file = request.files['file']
    file_metadata = {'name': file.filename}
    media = googleapiclient.http.MediaIoBaseUpload(file, mimetype=file.content_type)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    
    return jsonify({"message": f"Arquivo {file['name']} enviado com sucesso!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
