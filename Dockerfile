FROM python:3.10-slim

WORKDIR /app
COPY . /app

EXPOSE 80

CMD ["python", "sequential_server.py"]
