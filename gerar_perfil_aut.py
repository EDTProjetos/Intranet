import asyncio
from pyppeteer import launch
from pyppeteer.errors import TimeoutError
import time

async def run():
    try:
        # Inicia o navegador em modo headless
        browser = await launch(headless=True, args=[
            '--no-sandbox',
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--window-size=1920,1080',
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ])
        
        # Abre uma nova aba
        page = await browser.newPage()
        
        # Acesse a URL de login
        await page.goto("https://cobranca01.redeservice.com.br/cobranca.be.energia/Home/Login?ReturnUrl=%2Fcobranca.be.energia%2F")

        # Preenche os campos de login e senha
        await page.waitForSelector('[name="Login"]')
        await page.type('[name="Login"]', '220309')
        await page.waitForSelector('[name="Senha"]')
        await page.type('[name="Senha"]', '123456')

        # Clica no botão de login
        await page.click('button[type="submit"]')
        print("Login realizado com sucesso!")
        
        # Aguarda o carregamento da nova página
        await page.waitForNavigation()
        print("URL atual:", page.url)

        # Navega nos menus
        await page.waitForSelector('a:has-text("Processos Diários")')
        await page.click('a:has-text("Processos Diários")')

        await page.waitForSelector('a:has-text("Geração de Perfil")')
        await page.click('a:has-text("Geração de Perfil")')

        await page.waitForSelector('a:has-text("Novo")')
        await page.click('a:has-text("Novo")')
        print("Navegação concluída!")

        # Seleciona os checkboxes
        checkboxes = await page.querySelectorAll('table tr input[type="checkbox"]')
        
        # Seleciona os checkboxes 5 a 15
        for i, checkbox in enumerate(checkboxes[5:15], start=5):
            is_checked = await checkbox.getProperty('checked')
            if not is_checked:
                await checkbox.click()
                print(f"Checkbox {i} selecionado.")

        # Clica no botão "Iniciar"
        await page.waitForSelector('button:has-text("Iniciar")')
        await page.click('button:has-text("Iniciar")')
        print("Processo iniciado!")

        # Aguarda algum tempo (5 segundos)
        time.sleep(5)

    except TimeoutError as e:
        print(f"Erro ao executar o script: {e}")

    finally:
        await browser.close()
        print("Driver fechado.")

# Chama a função assíncrona para rodar
asyncio.get_event_loop().run_until_complete(run())
