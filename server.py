from flask import Flask, jsonify, render_template
import threading
import subprocess
import os

app = Flask(__name__)

script_finalizado = False

def executar_script():
    global script_finalizado
    script_finalizado = False
    script_path = r"Projetos Automatizados/Gerar perfil automático"  # Caminho completo para o script

    if os.path.exists(script_path):
        try:
            print(f"Executando script em: {script_path}")  # Log para verificar o caminho
            result = subprocess.run(
                ["python", script_path],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"Resultado do script: {result.stdout}")  # Exibe a saída do script
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar script: {e.output}")  # Exibe o erro se o script falhar

    else:
        print(f"O script não foi encontrado no caminho: {script_path}")
    
    script_finalizado = True
    print("Script finalizado.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/gerar-perfil")
def gerar_perfil():
    return render_template("gerar_perfil.html")

@app.route("/executar-script", methods=["POST"])
def executar_script_api():
    print("Requisição POST recebida!")  # Verifica se a requisição POST chegou
    thread = threading.Thread(target=executar_script)
    thread.start()
    return jsonify({"message": "Script iniciado, aguarde..."})

@app.route("/status", methods=["GET"])
def verificar_status():
    return jsonify({"script_finalizado": script_finalizado})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
