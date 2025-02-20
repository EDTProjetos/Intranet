FROM python:3.9-slim

# Instalar dependências do Chrome e do Selenium
RUN apt-get update && \
    apt-get install -y \
    wget \
    curl \
    unzip \
    ca-certificates \
    gnupg \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxrandr2 \
    libxss1 \
    libappindicator1 \
    libxtst6 \
    fonts-liberation \
    libgbm1 \
    libu2f-udev \
    lsb-release \
    xdg-utils \
    google-chrome-stable

# Instalar as dependências do Python
RUN pip install --no-cache-dir selenium webdriver-manager

# Copiar o código para o contêiner
COPY . /app

# Definir o diretório de trabalho
WORKDIR /app

# Comando para rodar o script
CMD ["python", "gerar_perfil_aut.py"]

RUN apt-get update && apt-get install -y wget curl unzip ca-certificates gnupg libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxrandr2 libxss1 libappindicator1 libxtst6 fonts-liberation libgbm1 libu2f-udev lsb-release xdg-utils

# Adicionando o repositório do Google Chrome
RUN curl -fsSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -y -f

