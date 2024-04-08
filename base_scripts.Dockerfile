# Stage 1: Build
FROM python:3.12 as build

WORKDIR /scripts
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim as runtime

WORKDIR /scripts
COPY --from=build /scripts /scripts

CMD ["python", "app.py"]