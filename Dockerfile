FROM python:3.9-slim

# Instalar dependências do Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg2 \
    ca-certificates \
    --no-install-recommends

# Adicionar o repositório do Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Instalar o Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable --no-install-recommends

# Instalar o ChromeDriver
RUN CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Configurações do seu projeto
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

# Defina a variável de ambiente
ENV CHROME_BIN=/usr/bin/google-chrome

# Expor a porta
EXPOSE 5000

# Comando para rodar o app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
