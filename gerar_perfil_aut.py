import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 🔹 Obtém o caminho do EdgeDriver do ambiente do Render
driver_path = os.getenv("EDGE_DRIVER_PATH", "/usr/bin/msedgedriver")

# 🔹 Inicializa o serviço do EdgeDriver
service = Service(driver_path)
edge_options = Options()

# 🔹 Configurações para rodar no Render
edge_options.add_argument("--headless")
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--no-sandbox")
edge_options.add_argument("--disable-dev-shm-usage")
edge_options.add_argument("--window-size=1920,1080")
edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# 🔹 Abre o navegador
driver = webdriver.Edge(service=service, options=edge_options)

try:
    print("Abrindo página de login...")
    driver.get("https://cobranca01.redeservice.com.br/cobranca.be.energia/Home/Login?ReturnUrl=%2Fcobranca.be.energia%2F")

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "Login"))).send_keys("220309")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "Senha"))).send_keys("123456")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
    print("Login realizado com sucesso!")

    time.sleep(5)
    print("URL atual:", driver.current_url)

    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Processos Diários"))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Geração de Perfil"))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Novo"))).click()
    print("Navegação concluída!")

    checkboxes = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, "//table//tr//input[@type='checkbox']"))
    )

    for i in range(5, 15):
        if not checkboxes[i].is_selected():
            checkboxes[i].click()
    print("Checkboxes selecionadas!")

    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Iniciar']"))
    ).click()
    print("Processo iniciado!")

except Exception as e:
    print(f"Erro: {e}")

finally:
    driver.quit()
    print("Driver fechado.")
