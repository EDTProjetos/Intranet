import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def executar_script():
    try:
        script_path = os.path.join(os.getcwd(), "Projetos Automatizados/Gerar perfil automático")
        
        if not os.path.exists(script_path):
            messagebox.showerror("Erro", "Script não encontrado no caminho especificado.")
            return
        
        # Executando o script
        subprocess.run(["python", script_path], check=True)
        
        # Exibindo mensagem de sucesso
        messagebox.showinfo("Sucesso", "Script executado com sucesso!")
    
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao executar o script: {e}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado: {e}")

# Criando a janela principal
root = tk.Tk()
root.title("Executar Script")
root.geometry("300x150")  # Tamanho da janela

# Adicionando um botão para executar o script
execute_button = tk.Button(root, text="Executar Script", command=executar_script)
execute_button.pack(pady=50)

# Iniciando o loop da interface gráfica
root.mainloop()
