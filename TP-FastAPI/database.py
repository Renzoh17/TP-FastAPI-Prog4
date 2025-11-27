import os
from typing import Generator

from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.sql.expression import Select, SelectOfScalar

# Deshabilita una advertencia común de SQLModel/SQLAlchemy
SelectOfScalar.inherit_cache = True
Select.inherit_cache = True

# -------------------------------------------------------------------
# Configuración del Motor
# -------------------------------------------------------------------

# Leer variables de entorno
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
# Construcción de la URL de conexión
# Nota: Utilizamos 'postgresql' (psycopg2)
DATABASE_URLV = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

DATABASE_URL = os.environ.get("DATABASE_URL") 

# El motor debe ser global y creado solo una vez
# echo=True para logging SQL en desarrollo
engine = create_engine(DATABASE_URL or DATABASE_URLV or "sqlite:///./local_temp.db", echo=True)


# -------------------------------------------------------------------
# Funciones de Base de Datos
# -------------------------------------------------------------------

def create_db_and_tables():
    """
    Crea el motor y luego las tablas.
    Esta función se llama durante el 'lifespan' de FastAPI.
    """
    global engine

    if not DATABASE_URL and not DATABASE_URLV:
        # Esto solo debería suceder si ejecutas fuera de Docker y sin variables de entorno
        print("ADVERTENCIA: DATABASE_URL no encontrada. Usando SQLite local.")
        # No es necesario crear el motor aquí si se crea arriba, pero es un buen patrón
        # para re-crear la conexión si fuera necesario.

    print("Intentando crear tablas en la base de datos...")
    
    # Esta línea ahora usa el motor creado. Si la URL era inválida, el fallo ocurrirá aquí.
    SQLModel.metadata.create_all(engine)
    print("Tablas verificadas/creadas exitosamente.")


def get_session() -> Generator[Session, None, None]:
    """
    Patrón de generador (Dependencia de FastAPI) para obtener una sesión.
    Abre una sesión y asegura que se cierre automáticamente.
    """
    with Session(engine) as session:
        yield session