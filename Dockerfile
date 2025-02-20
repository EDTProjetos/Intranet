# Base image: Python 3.9-slim
FROM python:3.9-slim

# Instalar dependências básicas e ferramentas
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    ca-certificates \
    gnupg \
    --no-install-recommends

# Adicionar a chave de assinatura e o repositório oficial do Google Chrome
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Atualizar o apt e instalar o Google Chrome junto com outras dependências necessárias
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
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
    xdg-utils

# Instalar as dependências do Python (Selenium, webdriver-manager, Flask e Gunicorn)
RUN pip install --no-cache-dir selenium webdriver-manager flask gunicorn

# Definir o diretório de trabalho e copiar o código do projeto
WORKDIR /app
COPY . /app

# Expor a porta do aplicativo (por exemplo, 5000)
EXPOSE 5000

# Comando para iniciar o servidor Flask com Gunicorn (supondo que o seu arquivo seja server.py e o app Flask esteja chamado "app")
CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]
