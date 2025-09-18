# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del SO necesarias (netcat para wait, gcc/libpq si se compila)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    netcat-traditional \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalarlas
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools && pip install -r /app/requirements.txt

# Copiar el código
COPY . /app/

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD gunicorn --chdir /app config.wsgi:application --bind 0.0.0.0:8000 --workers 3



