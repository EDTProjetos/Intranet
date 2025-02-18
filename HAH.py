from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuração do WebDriver para Microsoft Edge
edge_options = webdriver.EdgeOptions()
edge_options.add_argument("--start-maximized")  # Maximiza a janela
driver = webdriver.Edge(options=edge_options)

try:
    # URL de login
    url_login = "https://admin.solatioenergialivre.com.br/"
    driver.get(url_login)

    # Aguarda o campo de E-mail ser carregado
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-0")))

    # Credenciais de login
    usuario = "raphael.barbosa@energiadetodos.com.br"  # Substitua pelo seu e-mail
    senha = "Kon@rulind0."  # Substitua pela sua senha

    # Preencher os campos de E-mail e Senha
    driver.find_element(By.ID, "mat-input-0").send_keys(usuario)  # Preenche o e-mail
    driver.find_element(By.ID, "mat-input-1").send_keys(senha)  # Preenche a senha
    driver.find_element(By.ID, "mat-input-1").send_keys(Keys.RETURN)  # Pressiona Enter para logar

    # Aguarda o login ser processado (substitua pelo ID de um elemento que aparece após o login)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "elemento_apos_login")))
        print("Login realizado com sucesso!")
    except Exception as e:
        print(f"Erro ao esperar o carregamento após o login: {e}")

    # Acessa a página de atendimentos
    url_atendimentos = "https://admin.solatioenergialivre.com.br/#/list/Tickets?filter=%7B%22sort%22:%22timestamp%22,%22order%22:%22DESC%22%7D"
    driver.get(url_atendimentos)

    # Aguarda a página de atendimentos carregar
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "elemento_da_pagina_atendimentos")))
        print("Acesso à página de atendimentos concluído!")
    except Exception as e:
        print(f"Erro ao esperar o carregamento da página de atendimentos: {e}")

except Exception as e:
    print(f"Erro durante a execução do script: {e}")
finally:
    # Fecha o navegador
    driver.quit()