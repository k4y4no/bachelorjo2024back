FROM python:3.12.11-alpine3.22


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 8000


ENTRYPOINT ["uvicorn", "api.main:app","--host","0.0.0.0",  "--port", "8000"]