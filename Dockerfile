FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY StoreAPI/requirements.txt /app/StoreAPI/requirements.txt
RUN pip install --no-cache-dir -r /app/StoreAPI/requirements.txt

COPY . /app/

RUN mkdir -p /app/StoreAPI/logs

WORKDIR /app/StoreAPI

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]