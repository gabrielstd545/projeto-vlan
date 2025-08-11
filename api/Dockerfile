FROM python:3.9-slim

WORKDIR /app

# Instala dependências de sistema e limpa cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Healthcheck
HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando de execução alternativo (usando Flask para desenvolvimento)
CMD ["python", "app.py"]

# Para produção, descomente a linha abaixo após instalar o Gunicorn
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]