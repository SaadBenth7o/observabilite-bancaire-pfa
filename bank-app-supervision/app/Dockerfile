FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pip==24.2
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN mkdir -p /app/logs

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

EXPOSE 8000
CMD bash -lc 'for i in {1..30}; do python /app/run_migrations.py && break || echo "retry migrations..." && sleep 2; done; exec gunicorn -w 2 -b 0.0.0.0:8000 "wsgi:app"'
