FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

# Establece la carpeta donde está manage.py
WORKDIR /app/casapin

# Copia todos los archivos del proyecto
COPY . /app

# Instala dependencias desde la raíz
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Ejecuta gunicorn desde la carpeta del proyecto Django
CMD ["gunicorn", "casapin.wsgi:application", "--bind", "0.0.0.0:8000"]






