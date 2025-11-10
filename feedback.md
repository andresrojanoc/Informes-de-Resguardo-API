# Revisión de Prueba Técnica: Andrés Rojano

**Rol:** Desarrollador Backend Python/Django (con especialización en GIS)
**Fecha de Revisión:** 2025-11-10
**Revisor:** Equipo Q-Forest
**Enlace al Repositorio del Candidato:** `https://github.com/andresrojanoc/Informes-de-Resguardo-API`

---

## 1. Contexto y Misión de la Prueba Técnica

*   **Misión de la Prueba:** El objetivo de esta prueba era evaluar la capacidad del candidato para diseñar e implementar una API REST simple en Django, modelar datos, escribir código limpio y estructurado, y demostrar su dominio en el procesamiento de datos geoespaciales para resolver un problema de negocio específico.
*   **Problema Específico:** Se le pidió crear un microservicio para procesar datos de telemetría de maquinaria forestal. El servicio debía identificar "Informes de Resguardo" (apagados de motor fuera de turno), y utilizando un Shapefile de caminos, determinar si la ubicación del resguardo era segura (a más de 50 metros de un camino). La solución debía ser expuesta a través de una API REST y estar completamente dockerizada.

---

## 2. Checklist de Criterios de Evaluación

Se evalúa cada uno de los siguientes puntos asignando una puntuación de 1 (deficiente) a 5 (excelente). Se añade comentarios específicos que justifiquen la puntuación en la columna de "Observaciones".

---

### **A. Funcionalidad y Cumplimiento de Requisitos (¿Resuelve el problema?)**

| Criterio | Puntuación (1-5) | Observaciones |
| :--- | :--- | :--- |
| **Cumplimiento de Requisitos Básicos:** ¿La solución cumple con todos los requisitos funcionales explícitamente pedidos? | 1 | No. El requisito fundamental era utilizar **Django Ninja**, pero el candidato optó por **Django REST Framework**. Esta es una desviación crítica del stack tecnológico solicitado. Aunque los endpoints son funcionalmente similares, no se adhiere a la especificación técnica clave de la prueba. |
| **Manejo de Casos de Éxito:** ¿El "camino feliz" funciona como se espera? | 4 | La aplicación es funcional. |
| **Manejo de Casos de Borde/Errores:** ¿La API maneja entradas inválidas o situaciones de error de forma controlada? | 3 | El endpoint `PATCH` maneja adecuadamente los casos de `pk` no encontrado y de payload sin el campo `is_active`. Sin embargo, el endpoint `POST` carece de manejo de errores; una falla en el frágil script de parseo haría que el hilo de ejecución fallara silenciosamente sin notificar al cliente. |
| **Instrucciones de Uso:** ¿El `README.md` del candidato es claro y permite levantar y probar el proyecto sin dificultad? | 4 | El `README.md` es claro y está bien estructurado. Proporciona instrucciones detalladas para la configuración con Docker y ejemplos de `cURL` para cada endpoint. Este es uno de los puntos fuertes de la entrega. |

**Puntuación Parcial (Funcionalidad):** `12/20`

---

### **B. Calidad del Código y Arquitectura (¿Cómo lo resolvió?)**

| Criterio | Puntuación (1-5) | Observaciones |
| :--- | :--- | :--- |
| **Claridad y Legibilidad:** ¿El código es fácil de leer y entender? ¿Los nombres de variables y funciones son descriptivos? | 1 | La calidad del código en `processing/locations.py` es extremadamente baja. El parseo de los archivos XML se realiza mediante manipulación manual de strings y lectura línea por línea, en lugar de usar un parser XML estándar. El código es frágil, ineficiente y muy difícil de seguir debido a su lógica procedural compleja y al uso de múltiples variables de estado. |
| **Estructura del Proyecto:** ¿El proyecto sigue una estructura lógica y coherente (ej. separando modelos, vistas, etc.)? | 4 | La estructura del proyecto es coherente con las convenciones de Django y DRF. La separación de la aplicación (`processing`) y el proyecto (`resguardo_api`), y el uso de archivos como `serializers.py` y `urls.py` dentro de la app, es correcta. |
| **Principios de Diseño (SOLID/Clean):** ¿Demuestra una comprensión de la separación de responsabilidades? ¿La lógica de negocio está acoplada a la vista o está en una capa de servicio/caso de uso? | 4 | Hay un intento de separación, pero la ejecución es deficiente.|
| **Modelado de Datos:** ¿Los modelos de Django están bien definidos? ¿Usa los tipos de campo correctos? | 2 | Se utiliza SQLite, una base de datos no apta para entornos de producción o escalables. El modelo `InformeResguardo` es funcional, pero denota falta de atención al detalle (por ejemplo, `report_datetime` no es `auto_now_add`). |

**Puntuación Parcial (Calidad de Código):** `11/20`

---

### **C. Conocimientos Específicos del Rol (¿Domina las herramientas clave?)**

| Criterio | Puntuación (1-5) | Observaciones |
| :--- | :--- | :--- |
| **Uso del ORM de Django:** ¿Utiliza el ORM de forma eficiente o recurre a SQL crudo innecesariamente? | 3 | El uso del ORM es básico. Se implementa una lógica para evitar duplicados, lo cual es positivo. Sin embargo, la inserción de datos se realiza en un bucle (`objects.create`), lo que resulta en un problema de rendimiento de N+1 queries en lugar de utilizar una operación masiva como `bulk_create`. |
| **Implementación de API (Django Ninja/DRF):** ¿La API sigue las convenciones REST? ¿El manejo de peticiones y respuestas es correcto? | 1 | El candidato no utilizó Django Ninja, incumpliendo un requisito central. Aunque demuestra conocimiento de DRF, la implementación es básica. El no cumplir con el framework solicitado indica una falta de atención a los requerimientos técnicos o una incapacidad para aprender y aplicar una nueva herramienta. |
| **Uso de PostGIS:** **(CRÍTICO)** ¿Implementó correctamente el modelo con `GeometryField`? ¿Utilizó funciones espaciales (ej. `ST_Contains`) para resolver el problema geoespacial? | 4 | La implementación del análisis geoespacial con GeoPandas es uno de los pocos puntos sólidos. El código en la clase `Caminos` realiza correctamente la creación de un `Point`, la reproyección al sistema de coordenadas del shapefile y el cálculo de la distancia mínima. Demuestra una comprensión funcional del problema GIS. |
| **Testing:** ¿Incluyó tests unitarios o de integración? ¿Los tests son significativos? | 1 | El archivo `tests.py` está vacío. No se proporcionó ninguna prueba automatizada. |

**Puntuación Parcial (Conocimientos Específicos):** `9/20`
### **Puntuación Total:** `32` / 60