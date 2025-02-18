import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 🔹 Verifica o caminho do EdgeDriver, pode ser configurado como variável de ambiente no Render
driver_path = os.getenv("EDGE_DRIVER_PATH", "/usr/bin/msedgedriver")  # Usando variável de ambiente

# 🔹 Inicializa o serviço do EdgeDriver
service = Service(driver_path)
edge_options = Options()

# 🔹 Configurações para modo headless no Render
edge_options.add_argument("--headless")
edge_options.add_argument("--disable-gpu")  # Necessário para compatibilidade
edge_options.add_argument("--window-size=1920,1080")  # Evita problemas de renderização
edge_options.add_argument("--start-maximized")
edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# 🔹 Abre o navegador
driver = webdriver.Edge(service=service, options=edge_options)

try:
    print("Página carregada! Tentando login...")

    driver.get("https://cobranca01.redeservice.com.br/cobranca.be.energia/Home/Login?ReturnUrl=%2Fcobranca.be.energia%2F")

    # 🔹 Login
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "Login"))).send_keys("220309")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "Senha"))).send_keys("123456")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
    print("Login realizado!")

    # 🔹 Aguarda redirecionamento para DashBoard
    time.sleep(5)  # Garante tempo para a página carregar
    print("URL atual:", driver.current_url)

    # 🔹 Navegação dentro do site
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Processos Diários"))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Geração de Perfil"))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Novo"))).click()
    print("Navegação concluída!")

    # 🔹 Seleciona as checkboxes
    checkboxes = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, "//table//tr//input[@type='checkbox']"))
    )

    for i in range(5, 15):
        if not checkboxes[i].is_selected():
            checkboxes[i].click()
    print("Checkboxes selecionadas!")

    # 🔹 Clica no botão 'Iniciar'
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Iniciar']"))
    ).click()
    print("Processo iniciado com sucesso!")

except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    driver.quit()
    print("Driver fechado.")
