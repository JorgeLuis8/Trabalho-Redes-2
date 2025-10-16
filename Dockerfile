FROM ubuntu:24.04

# Python + venv + deps nativos
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Virtualenv para pacotes Python (numpy, pandas, matplotlib)
RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install --upgrade pip \
 && /opt/venv/bin/pip install numpy pandas matplotlib

ENV PATH="/opt/venv/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

# O comando é definido pelo docker-compose para cada serviço
CMD ["python3", "executar_experimentos.py"]
