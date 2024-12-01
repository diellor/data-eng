# Use Python 3.12 as the base image
FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/wait-for-db.sh

CMD ["sh", "-c", "./wait-for-db.sh db python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
