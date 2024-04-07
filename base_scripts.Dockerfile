FROM python:3.12-bullseye
RUN pip install minio pika redis
WORKDIR /scripts
ENTRYPOINT python app.py