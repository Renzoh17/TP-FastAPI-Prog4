import logging
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool
from sqlmodel import create_engine, SQLModel, Session
from typing import Generator

# Basic Logging Configuration (Optional)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    #Environment Variables BDD
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    
    #Aplication Mode (echo controller)
    ENVIRONMENT: str = "development"
    
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB
        )
        
    class Config:
        env_file = ".env" # Load .env if exists
        extra = "ignore"
        
# Configuration Instance
settings = Settings()

# Determinate if can see logging SQL (in development)
echo_sql = settings.ENVIRONMENT == "development"

# Create Motor SQLModel
engine: Engine = create_engine(
    str(settings.DATABASE_URL),
    echo=echo_sql, # View querys in console in development mode
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True, # Verify connections before use
    pool_recycle=300 # Recycle connections for 5 minutes
)

def create_db_and_tables():
    logger.info("Creando tables en la Base de datos")
    SQLModel.metadata.create_all(engine)
    logger.info("Tablas creadas correctamente")
    
def get_session() -> Generator[Session, None, None]:
    "Session Generator"
    with Session(engine) as session:
        yield session

