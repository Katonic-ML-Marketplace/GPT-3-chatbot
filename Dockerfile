FROM python:3.8.2-slim

COPY app.py .
COPY assets assets
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD gunicorn app:server -b 0.0.0.0:8050
