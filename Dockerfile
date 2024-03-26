#Deriving the base image
FROM python:3.10-slim-bullseye

# Crear un entorno virtual
RUN python -m venv /opt/env

# Activar el entorno virtual
ENV PATH="/opt/venv/bin:$PATH"

# Establecer el directorio de trabajo en el contenedor
WORKDIR /usr/app/src

# Copiar los archivos necesarios al contenedor
COPY requirements.txt .
COPY main.py .
COPY .env .
COPY schemas.py .
COPY resources/ ./resources/
COPY pdf/ ./pdf/

# Instalar las dependencias
RUN pip install --no-cache -r requirements.txt

# Etiqueta para el mantenedor de la imagen
LABEL Maintainer="Camilo Campos"

# Comando para ejecutar la aplicación
CMD [ "python", "./main.py"]