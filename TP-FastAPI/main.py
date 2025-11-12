import os
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager

# --- Cargar Variables de Entorno al inicio ---
# Debe llamarse antes de importar cualquier módulo que dependa de ellas
load_dotenv()


# --- Importación de Componentes del Proyecto ---
# 1. Importar los modelos para que SQLModel los registre
import models 

# 2. Importar la función de creación de tablas
from database import create_db_and_tables

# 3. Importar los Routers
from autos import router as autos_router
from ventas import router as ventas_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Función que se ejecuta al inicio (startup) y al cierre (shutdown) de la aplicación.
    """
    # --- Startup ---
    print("Aplicación iniciando...")
    # Creamos las tablas en la base de datos si no existen
    create_db_and_tables()
    yield
    # --- Shutdown ---
    print("Aplicación cerrando...")
    # Aquí podrías añadir cualquier lógica de limpieza si fuera necesaria


# --- Inicialización de FastAPI ---

app = FastAPI(
    title="API de Gestión de Autos y Ventas",
    version="1.0.0",
    description="API RESTful construida con FastAPI y SQLModel para gestionar un inventario de vehículos y su historial de ventas.",
    lifespan=lifespan # Usamos la función de ciclo de vida
)


# --- Inclusión de Routers ---

app.include_router(autos_router)
app.include_router(ventas_router)


# --- Endpoint Raíz (Opcional) ---

@app.get("/")
def read_root():
    """
    Endpoint de prueba para verificar que la API esté funcionando.
    """
    return {"message": "Bienvenido a la API de Gestión de Autos y Ventas. Visita /docs para la documentación."}

# Nota: Para correr esta aplicación, usarás un servidor ASGI como Uvicorn:
# uvicorn main:app --reload