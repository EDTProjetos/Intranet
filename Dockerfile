FROM python:3.9

RUN apt-get update && apt-get install -y \
    wget curl unzip xvfb \
    ca-certificates fonts-liberation libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libcups2 \
    libdbus-1-3 libdrm2 libgbm1 libnspr4 libnss3 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libxrender1 libxss1 libxtst6 chromium-browser \
    && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN="/usr/bin/chromium-browser"
ENV PATH="/usr/bin/chromium-browser:$PATH"

RUN CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -q https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip -O chromedriver.zip && \
    unzip chromedriver.zip && \
    mv chromedriver /usr/bin/ && \
    chmod +x /usr/bin/chromedriver && \
    rm chromedriver.zip

RUN echo "Google Chrome Version:" && $CHROME_BIN --version
RUN echo "ChromeDriver Version:" && chromedriver --version

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
