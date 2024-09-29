# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requerimientos
COPY requirements.txt .

# Actualizar pip a la última versión
RUN pip install --upgrade pip

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto Django al contenedor
COPY . /app

#Establece la variable de entorno para Django
ENV DJANGO_SETTINGS_MODULE=maplinker.settings

RUN python manage.py collectstatic --noinput


#Exponer el puerto que el servidor de desarrollo usará
EXPOSE 8000

# Ejecutar el servidor de desarrollo

CMD ["uvicorn", "maplinker.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
