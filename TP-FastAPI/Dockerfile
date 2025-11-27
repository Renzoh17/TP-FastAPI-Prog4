# 1. IMAGEN BASE
# Usamos una imagen oficial de Python basada en Alpine Linux, que es muy pequeña
# y eficiente. Esto reduce el tamaño final del contenedor.
FROM python:3.12-slim-bookworm

# 2. DIRECTORIO DE TRABAJO
# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. COPIAR REQUISITOS E INSTALAR DEPENDENCIAS
# Copia solo el archivo de requisitos primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instala todas las dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. COPIAR CÓDIGO DE LA APLICACIÓN
# Copia el resto del código fuente del proyecto al directorio de trabajo /app
COPY . .

# 5. EXPONER PUERTO
# Le dice a Docker qué puerto usará el contenedor (FastAPI/Uvicorn usa 8000 por defecto)
EXPOSE 8000

# 6. COMANDO DE INICIO
# Define el comando para iniciar la aplicación usando Uvicorn
# El formato es: uvicorn <nombre_del_módulo>:<nombre_de_la_instancia_de_FastAPI> --host 0.0.0.0 --port 8000
# Asumiendo que en 'main.py' tienes 'app = FastAPI()'
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]