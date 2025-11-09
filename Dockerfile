# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Evita prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Crea y usa el directorio de la app
WORKDIR /app

# Instala dependencias del sistema necesarias para GDAL y GeoPandas
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    build-essential \
    python3-dev \
    libgeos-dev \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# Configura variables necesarias para GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Copia requirements.txt e instala dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Expone el puerto de Django
EXPOSE 8000

# Comando por defecto para correr Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
