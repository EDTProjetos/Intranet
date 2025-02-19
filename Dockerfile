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

# 🔹 Instala Microsoft Edge e msedgedriver
RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add - && \
    echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" | tee /etc/apt/sources.list.d/microsoft-edge.list && \
    apt-get update && \
    apt-get install -y microsoft-edge-stable

RUN wget -O /usr/bin/msedgedriver https://msedgedriver.azureedge.net/120.0.2210.91/edgedriver_linux64.zip && \
    unzip /usr/bin/msedgedriver -d /usr/bin/ && \
    chmod +x /usr/bin/msedgedriver

# Define a pasta do projeto
WORKDIR /app

# Copia os arquivos do projeto
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

# Expõe a porta do Flask
EXPOSE 5000

# Variável de ambiente para o caminho do EdgeDriver
ENV EDGE_DRIVER_PATH="/usr/bin/msedgedriver"

# Comando para iniciar o servidor Flask
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
