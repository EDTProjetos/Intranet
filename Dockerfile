# Base image: Python 3.9-slim
FROM python:3.9-slim

# Instalar dependências do sistema e do Chrome
RUN apt-get update && apt-get install -y \
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
    xdg-utils

# Adiciona o repositório oficial do Google Chrome e instala o Google Chrome Stable
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Instalar dependências do Python
RUN pip install --no-cache-dir selenium webdriver-manager flask gunicorn

# Copiar o código da aplicação para o contêiner
WORKDIR /app
COPY . /app

# Expor a porta que o Flask irá usar
EXPOSE 5000

# Comando para iniciar o servidor Flask com Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]
