FROM python:3.12-slim


WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev build-essential --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
    
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 8080


ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]