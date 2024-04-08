FROM python:3.12-alpine
RUN pip install minio pika redis
WORKDIR /scripts
ENTRYPOINT python app.py