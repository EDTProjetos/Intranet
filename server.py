from flask import Flask, jsonify, render_template
import threading
import subprocess
import os
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

app = Flask(__name__)

script_finalizado = False

def baixar_msedgedriver():
    """Baixa e configura automaticamente o msedgedriver para o Selenium"""
    print("Baixando msedgedriver...")
    try:
        driver_path = EdgeChromiumDriverManager().install()
        print(f"msedgedriver baixado em: {driver_path}")
        return driver_path
    except Exception as e:
        print(f"Erro ao baixar msedgedriver: {str(e)}")
        return None

def verificar_versao_msedgedriver():
    """Inicia o Edge WebDriver e exibe a versão instalada"""
    print("Verificando versão do msedgedriver...")

    driver_path = baixar_msedgedriver()
    if not driver_path:
        print("Erro ao obter msedgedriver.")
        return

    options = webdriver.EdgeOptions()
    options.add_argument("--headless")  # Executar sem interface gráfica
    options.add_argument("--disable-gpu")  
    options.add_argument("--no-sandbox")
    options.add_argument("--user-data-dir=/tmp/msedgedriver-data")  # Evita erro de diretório em uso

    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=options)

    version = driver.capabilities['browserVersion']
    msedgedriver_version = driver.capabilities['msedgedriverVersion']

    print(f"Versão do navegador Edge: {version}")
    print(f"Versão do msedgedriver: {msedgedriver_version}")

    driver.quit()

def executar_script():
    """Executa o script Python 'gerar_perfil_aut.py' em uma thread separada"""
    global script_finalizado
    script_finalizado = False
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(BASE_DIR, "gerar_perfil_aut.py")
    
    if os.path.exists(script_path):
        try:
            print(f"Executando script em: {script_path}")
            result = subprocess.run(
                ["python3", script_path],  # "python3" para garantir compatibilidade no servidor
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
    
    print("Script finalizado.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/gerar-perfil")
def gerar_perfil():
    return render_template("gerar_perfil.html")

@app.route("/executar-script", methods=["POST"])
def executar_script_api():
    print("Requisição POST recebida! Iniciando script...")
    thread = threading.Thread(target=executar_script)
    thread.start()
    return jsonify({"message": "Script iniciado, aguarde..."})

@app.route("/status", methods=["GET"])
def verificar_status():
    return jsonify({"script_finalizado": script_finalizado})

@app.route("/verificar-driver", methods=["GET"])
def api_verificar_versao_msedgedriver():
    """Endpoint para verificar a versão do msedgedriver via API"""
    verificar_versao_msedgedriver()
    return jsonify({"message": "Verificação concluída! Veja os logs para detalhes."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render usa a variável PORT
    app.run(host="0.0.0.0", port=port)
