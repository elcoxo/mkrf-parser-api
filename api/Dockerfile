FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/api
COPY .env .

WORKDIR /app/api
CMD ["bash", "-c", "python manage.py makemigrations register_movies \
&& python manage.py migrate && python manage.py runserver 0.0.0.0:8001"]







