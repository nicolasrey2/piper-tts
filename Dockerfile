# Usamos una base ligera con Python
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Puerto por defecto
ENV TTS_PORT=8000


# configuramos zona horaria
ENV TZ=America/Argentina/Buenos_Aires
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


# Instalo sox
RUN apt-get update && apt-get install -y \
    sox \
    libsox-fmt-all \
    && rm -rf /var/lib/apt/lists/*


# Carpeta de trabajo
WORKDIR /app

# Instalamos dependencias
COPY app/ .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install piper-tts

# Creamos carpeta para audios
RUN mkdir -p /outputs

# Copiamos los modelos de Piper al contenedor
RUN mkdir -p /voces
COPY voces/ /voces/

# Exponemos puerto
EXPOSE ${TTS_PORT}

ENV PYTHONPATH=/app/src


# Comando por defecto
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $TTS_PORT"]