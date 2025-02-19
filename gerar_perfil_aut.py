import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Obtém os caminhos do Chrome e do ChromeDriver
chrome_binary = os.getenv("CHROME_BIN", "/usr/bin/google-chrome")
chromedriver_path = os.getenv("CHROMEDRIVER_PATH", ChromeDriverManager().install())

# Inicializa o serviço do ChromeDriver
service = Service(chromedriver_path)

# Configurações para o Chrome
chrome_options = Options()
chrome_options.binary_location = chrome_binary
chrome_options.add_argument("--headless")  # Modo sem interface gráfica
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Inicializa o WebDriver
try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("ChromeDriver iniciado com sucesso!")

    print("Abrindo página de login...")
    driver.get("https://cobranca01.redeservice.com.br/cobranca.be.energia/Home/Login?ReturnUrl=%2Fcobranca.be.energia%2F")

    # Preenche os campos de login e senha
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "Login"))).send_keys("220309")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "Senha"))).send_keys("123456")

    # Clica no botão de login
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
    print("Login realizado com sucesso!")

    time.sleep(5)  # Aguarda carregamento da página
    print("URL atual:", driver.current_url)

    # Navega nos menus
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Processos Diários"))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Geração de Perfil"))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Novo"))).click()
    print("Navegação concluída!")

    # Seleciona checkboxes
    checkboxes = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, "//table//tr//input[@type='checkbox']"))
    )
    
    for i, checkbox in enumerate(checkboxes[5:15], start=5):
        if not checkbox.is_selected():
            checkbox.click()
            print(f"Checkbox {i} selecionado.")

    # Clica no botão "Iniciar"
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Iniciar']"))
    ).click()
    print("Processo iniciado!")

except Exception as e:
    print(f"Erro ao executar o script: {e}")

finally:
    if 'driver' in locals():
        driver.quit()
        print("Driver fechado.")
