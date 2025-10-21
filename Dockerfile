FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
      python3 python3-pip python3-venv \
      gcc \
    && pip3 install --no-cache-dir matplotlib \
    && apt-get clean

WORKDIR /app
COPY . /app

EXPOSE 80
CMD ["python3"]
