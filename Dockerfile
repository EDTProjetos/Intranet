# Usa a imagem do Python como base
FROM python:3.9

# Instala pacotes essenciais
RUN apt-get update && apt-get install -y \
    wget curl unzip xvfb \
    ca-certificates fonts-liberation libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libcups2 \
    libdbus-1-3 libdrm2 libgbm1 libnspr4 libnss3 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libxrender1 libxss1 libxtst6 \
    && rm -rf /var/lib/apt/lists/*

# 🔹 Instala o Google Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome.deb && \
    dpkg -i google-chrome.deb && \
    apt-get -y install -f && \
    rm google-chrome.deb

# 🔹 Instala o ChromeDriver
RUN wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip -O chromedriver.zip && \
    unzip chromedriver.zip && \
    mv chromedriver /usr/bin/ && \
    chmod +x /usr/bin/chromedriver && \
    rm chromedriver.zip

# Define a pasta do projeto
WORKDIR /app

# Copia os arquivos do projeto
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

# Expõe a porta do Flask
EXPOSE 5000

# Variável de ambiente para o caminho do ChromeDriver
ENV CHROME_DRIVER_PATH="/usr/bin/chromedriver"

# Comando para iniciar o servidor Flask
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
