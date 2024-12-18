# Imagen base de Python
FROM python:3.12.8-slim

# Directorio de trabajo
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que corre la aplicación
EXPOSE 8501

# Comando para ejecutar la aplicación
CMD ["shiny", "run", "app.py"]
