# Use uma imagem base do Ubuntu ou Debian
FROM ubuntu:20.04

# Atualizar pacotes e instalar dependências para o Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    ca-certificates \
    libx11-dev \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libnspr4 \
    libnss3 \
    libxss1 \
    fonts-liberation \
    libappindicator3-1 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libgtk-3-0 \
    xdg-utils \
    --no-install-recommends

# Baixar e instalar o Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb && \
    apt-get -f install -y

# Definir o caminho do Chrome
ENV CHROME_BIN=/usr/bin/google-chrome-stable

# Instalar o ChromeDriver
RUN apt-get install -y chromium-driver

# Instalar dependências para o Python e o Selenium
RUN apt-get install -y python3-pip && \
    pip3 install selenium webdriver-manager

# Expor a porta em que o seu serviço estará rodando (se necessário)
EXPOSE 5000

# Comando padrão para rodar o aplicativo (caso necessário)
# CMD ["python3", "app.py"]
