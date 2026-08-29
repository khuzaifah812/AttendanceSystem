FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y pkg-config default-libmysqlclient-dev build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/staticfiles
RUN python manage.py collectstatic --noinput || true
RUN adduser --disabled-password --no-create-home appuser
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT