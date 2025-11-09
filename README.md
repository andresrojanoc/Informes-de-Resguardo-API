# Informes de Resguardo API

API desarrollada con **Django REST Framework** para procesar datos de ubicación y generar informes de resguardo a partir de archivos XML y shapefiles.

---

## Requisitos Previos

Antes de comenzar, asegurese de tener instalados:

* **Docker Desktop** (Windows, macOS o Linux)
* **WSL 2** habilitado (si usas Windows)
* **Docker Compose v2**

Verifica la instalación con:

```bash
docker compose version
```

Deberías ver algo similar a:

```
Docker Compose version v2.40.3-desktop.1 
```

---

## Configuración del Entorno

### Clona este repositorio o copia el proyecto a tu entorno local

```bash
git clone https://github.com/andresrojanoc/Informes-de-Resguardo-API.git
cd Informes-de-Resguardo-API/
```

### Asegúrate de que los siguientes archivos estén en la raíz del proyecto

```
resguardo_api/
├── Dockerfile
├── README.md
├── data
│   ├── EngineStatusMessages-844585.xml 
│   ├── LocationMessages-844585-page_2.xml 
│   ├── LocationMessages-844585-page_2.xml 
│   ├── CAMINOS_7336.dbf
│   ├── CAMINOS_7336.prj 
│   ├── CAMINOS_7336.shp 
│   ├── CAMINOS_7336.shx 
│   └── ...
├── docker-compose.yml
├── manage.py
├── requirements.txt
├── processing/
│   ├── locations.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── ...
├── resguardo_api
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
```

### Construye la imagen Docker

```bash
docker compose build
```

### Levanta los contenedores

```bash
docker compose up
```

El servidor Django se iniciará dentro del contenedor y estará disponible en:

 [http://localhost:8000](http://localhost:8000)

---

## Endpoints Principales

### 1️ Procesamiento de datos

Ejecuta el procesamiento de archivos XML y Shapefile.

**POST** `/data-processing/`

```bash
curl -X POST http://localhost:8000/data-processing/
```

**Respuesta esperada:**

```json
{"message": "Data processing initiated successfully."}
```

---

### 2️ Consultar informes

Lista los informes de resguardo activos.

**GET** `/safeguard-reports/`

```bash
curl -X GET http://localhost:8000/safeguard-reports/
```

**Ejemplo de respuesta:**

```json
[
  {
    "id": 1,
    "machine_serial": "844585",
    "report_datetime": "2024-11-04T21:05:00Z",
    "engine_off_timestamp": "2024-11-04T20:05:00Z",
    "is_safe": false,
    "lat": -37.12345,
    "lon": -72.56789,
    "distance_to_road_m": 35.5,
    "is_active": true
  }
]
```

---

### 3️ Borrado suave (soft delete)

Desactiva un informe sin eliminarlo físicamente.

**PATCH** `/safeguard-reports/{id}/`

```bash
curl -X PATCH http://127.0.0.1:8000/safeguard-reports/1/ \
     -H "Content-Type: application/json" \
     -d '{"is_active": false}'
```

**Respuesta esperada:**

```json
{
  "id": 1,
  "machine_serial": "844585",
  "is_active": false
}
```

---

## Mantenimiento

Para detener los contenedores:

```bash
docker compose down
```

Para reconstruir la imagen desde cero:

```bash
docker compose build --no-cache
```

Para acceder al contenedor Django:

```bash
docker compose exec web bash
```

---

## Notas

* Los archivos XML y el shapefile deben estar presentes en el directorio /data/ del proyecto.
* Si un informe ya existe y fue desactivado (`is_active = False`), el sistema **lo reactivará** en lugar de crear un duplicado.
* Librerías clave del entorno:

  * **GeoPandas**
  * **Shapely**
  * **GDAL**
  * **Django REST Framework**

---
