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
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# El motor debe ser global y creado solo una vez
# echo=True para logging SQL en desarrollo
engine = create_engine(DATABASE_URL, echo=True)


# -------------------------------------------------------------------
# Funciones de Base de Datos
# -------------------------------------------------------------------

def create_db_and_tables():
    """
    Crea las tablas en la base de datos.
    Si las tablas ya existen, no hace nada.
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