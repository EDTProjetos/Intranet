FROM python:3.9

# Instala dependências
RUN apt-get update && apt-get install -y \
    wget unzip curl \
    && rm -rf /var/lib/apt/lists/*

# Instala Chrome e ChromeDriver
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Instala dependências Python
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do Flask
COPY . /app

# Expõe a porta Flask
EXPOSE 5000

# Roda a aplicação Flask
CMD ["python", "app.py"]