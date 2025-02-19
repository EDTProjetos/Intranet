from flask import Flask, jsonify, render_template
import threading
import subprocess
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

app = Flask(__name__)

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
