from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
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

    # Aguarda o login ser processado
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='dashboard']")))
    print("Login realizado com sucesso!")

    # Acessa a página de pagamentos
    url_pagamentos = "https://admin.solatioenergialivre.com.br/#/list/EnergyMeterPayments"
    driver.get(url_pagamentos)

    # Aguarda a página de pagamentos carregar
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//h3[@title='Data de pagamento']"))
    )
    print("Acesso à página de pagamentos concluído!")

    # Definir o intervalo de datas para o filtro
    hoje = datetime.today()
    primeiro_dia_mes = hoje.replace(day=1)
    dia_anterior = hoje - timedelta(days=1)

    data_inicio = primeiro_dia_mes.strftime("%Y-%m-%d")
    data_fim = dia_anterior.strftime("%Y-%m-%d")

    print(f"Data início: {data_inicio}, Data fim: {data_fim}")

    # Localizar e preencher os campos de data
    campo_data_inicio = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Data inicial']"))
    )
    campo_data_fim = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Data final']"))
    )

    campo_data_inicio.clear()
    campo_data_inicio.send_keys(data_inicio)

    campo_data_fim.clear()
    campo_data_fim.send_keys(data_fim)

    # Localizar e clicar no botão "Aplicar filtro"
    botao_aplicar_filtros = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Aplicar_filtros')]"))
    )
    botao_aplicar_filtros.click()

    # Aguarda os resultados serem carregados após o filtro
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//table[@id='tabela_resultados']"))
    )
    print("Resultados filtrados carregados!")

except Exception as e:
    print(f"Erro durante a execução do script: {e}")

finally:
    # Fecha o navegador
    driver.quit()
