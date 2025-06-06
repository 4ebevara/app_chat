FROM python:3.11-slim

WORKDIR /app

# Установка bash и netcat для wait-for-it.sh
RUN apt-get update && apt-get install -y bash netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Копируем скрипт wait-for-it.sh и даём права на выполнение
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

CMD ["/wait-for-it.sh", "db", "5432", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
