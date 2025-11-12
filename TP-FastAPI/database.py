import os
from typing import Generator

from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.sql.expression import Select, SelectOfScalar

# Deshabilita una advertencia común de SQLModel/SQLAlchemy
SelectOfScalar.inherit_cache = True
Select.inherit_cache = True

# -------------------------------------------------------------------
# 1. Configuración del Motor
# -------------------------------------------------------------------

# Leer variables de entorno (asumimos que load_dotenv() se llama en main.py)
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "admin")
POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "autos_db")
# Construcción de la URL de conexión
# Nota: Utilizamos 'postgresql' (psycopg2) en lugar de 'postgresql+psycopg2'
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# El motor debe ser global y creado solo una vez
# echo=True para logging SQL en desarrollo
engine = create_engine(DATABASE_URL, echo=True)


# -------------------------------------------------------------------
# 2. Funciones de Base de Datos
# -------------------------------------------------------------------

def create_db_and_tables():
    """
    Crea las tablas en la base de datos.
    Debe ser llamada después de que todos los modelos hayan sido importados
    (usualmente al inicio de main.py).
    """
    print("Intentando crear tablas en la base de datos...")
    # SQLModel.metadata contiene la definición de todas las tablas
    # creadas a partir de las clases SQLModel importadas.
    SQLModel.metadata.create_all(engine)
    print("Tablas verificadas/creadas exitosamente.")


def get_session() -> Generator[Session, None, None]:
    """
    Patrón de generador (Dependencia de FastAPI) para obtener una sesión.
    Abre una sesión y asegura que se cierre automáticamente.
    """
    with Session(engine) as session:
        yield session