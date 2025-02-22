# Imagem base
FROM python:3.9-slim

# Instalar ferramentas básicas necessárias para adicionar repositórios e baixar pacotes
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

# Atualizar e instalar o Google Chrome
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

# Instalar as dependências do Python necessárias para o seu projeto
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Definir o diretório de trabalho e copiar o código da aplicação
WORKDIR /app
COPY . /app

# Expor a porta que sua aplicação Flask usará
EXPOSE 5000

# Comando para iniciar o servidor Flask com Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]
