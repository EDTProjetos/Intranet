from flask import Flask, jsonify, render_template
import threading
import subprocess
import os

app = Flask(__name__)

script_finalizado = False

def executar_script():
    global script_finalizado
    script_finalizado = False
    
    # Descobre a pasta base onde está este arquivo
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Monta o caminho para o script Python correto
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
            
            if result.returncode != 0:
                print(f"Erro ao executar o script: {result.stderr}")
                script_finalizado = False
            else:
                script_finalizado = True
                print("Script executado com sucesso!")

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
    print("Requisição POST recebida!")
    thread = threading.Thread(target=executar_script)
    thread.start()
    return jsonify({"message": "Script iniciado, aguarde..."})

@app.route("/status", methods=["GET"])
def verificar_status():
    return jsonify({"script_finalizado": script_finalizado})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render usa a variável PORT
    app.run(host="0.0.0.0", port=port)
