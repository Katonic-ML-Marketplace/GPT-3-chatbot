FROM python:3.8.2-slim

RUN mkdir -p assets

COPY app.py .
COPY assets/logo.png assets/.
COPY assets/favicon.ico assets/.
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD python app.py --server.port=8050 --server.address=0.0.0.0 --logger.level error --server.fileWatcherType=none
