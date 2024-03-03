# Pull de la imagen base oficial
FROM python:3.10.13-alpine

# setup del directorio de trabajo
WORKDIR /app

# Configuración de las variables de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt


COPY . ./app/

CMD ["uvicorn", "main:app", "--reload","--host", "0.0.0.0", "--port", "8000"]