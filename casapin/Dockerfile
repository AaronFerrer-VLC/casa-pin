FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del código del proyecto
COPY . .

# Comando de arranque
CMD ["gunicorn", "casapin.wsgi:application", "--bind", "0.0.0.0:8000"]
