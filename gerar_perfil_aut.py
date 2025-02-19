import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 🔹 Inicializa o serviço do ChromeDriver
service = Service(ChromeDriverManager().install())

# 🔹 Configurações para o Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Sem interface gráfica
chrome_options.add_argument("--disable-gpu")  # Desabilitar GPU (recomendado para headless)
chrome_options.add_argument("--no-sandbox")  # Necessário em alguns servidores
chrome_options.add_argument("--disable-dev-shm-usage")  # Evitar erro em alguns ambientes de nuvem
chrome_options.add_argument("--window-size=1920,1080")  # Definir resolução
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")  # User agent

# 🔹 Abre o navegador
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print("Abrindo página de login...")
    driver.get("https://cobranca01.redeservice.com.br/cobranca.be.energia/Home/Login?ReturnUrl=%2Fcobranca.be.energia%2F")
    
    # Espera até que os campos de login estejam presentes e preenche as credenciais
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "Login"))).send_keys("220309")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "Senha"))).send_keys("123456")
    
    # Clica no botão de login
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
    print("Login realizado com sucesso!")

    # Aguarda e imprime a URL atual para confirmação
    time.sleep(5)
    print("URL atual:", driver.current_url)

    # Navega até os menus subsequentes
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Processos Diários"))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Geração de Perfil"))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Novo"))).click()
    print("Navegação concluída!")

    # Aguarda até que as checkboxes estejam presentes
    checkboxes = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, "//table//tr//input[@type='checkbox']"))
    )

    # Seleciona checkboxes entre o índice 5 e 15, se não estiverem selecionadas
    for i in range(5, 15):
        if not checkboxes[i].is_selected():
            checkboxes[i].click()
    print("Checkboxes selecionadas!")

    # Clica no botão "Iniciar"
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Iniciar']"))
    ).click()
    print("Processo iniciado!")

except Exception as e:
    print(f"Erro: {e}")

finally:
    driver.quit()
    print("Driver fechado.")
