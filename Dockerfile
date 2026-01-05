# Usa la imagen oficial de Python 3.12 liviana basada en Debian
FROM python:3.12-slim

# Documenta que el contenedor escuchará en el puerto 8000 (informativo)
EXPOSE 8000

# Define el directorio de trabajo dentro del contenedor. 
# Todo comando posterior se ejecutará aquí.
WORKDIR /code

# Copia solo el archivo de requisitos primero para aprovechar la caché de capas de Docker
COPY ./requirements.txt /code/requirements.txt

# Instala las dependencias. --no-cache-dir evita guardar archivos temporales, 
# haciendo la imagen más ligera.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia el código de tu aplicación (la carpeta app) al directorio /code/app
COPY ./app /code/app

# Comando que arranca la API. 
# --proxy-headers es vital si luego usas un Load Balancer o Nginx. Le dice a FastAPI: "Confía en las cabeceras que te envía el Load Balancer", evitando errores al generar URLs o validar protocolos de seguridad.
# --host Le dice al servidor que escuche en todas las interfaces de red del contenedor. Si pusieras 127.0.0.1, el contenedor solo se escucharía a sí mismo y el mundo exterior (mediante el LB) no podrían entrar.
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]