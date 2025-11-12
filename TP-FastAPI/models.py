from datetime import datetime
from typing import List, Optional
import re

# Importamos las clases necesarias de SQLModel, incluyendo el validador
from sqlmodel import Field, Relationship, SQLModel

from pydantic import field_validator


# Obtener el año actual una sola vez para la validación de 'Auto'
CURRENT_YEAR = datetime.now().year


# ====================================================================
# --- 1. Modelos de Venta (Many side) ---
# ====================================================================

# VentaBase: Campos comunes con validaciones Pydantic
class VentaBase(SQLModel):
    nombre_comprador: str = Field(min_length=1, description="El nombre del comprador no puede estar vacío.")
    precio: float = Field(gt=0, description="El precio de venta debe ser mayor a 0.")
    # Clave foránea que enlaza esta Venta con el Auto
    auto_id: Optional[int] = Field(default=None, foreign_key="auto.id")
    # Usamos UTC por defecto para la consistencia
    fecha_venta: datetime = Field(default_factory=datetime.now())

    # Validador para asegurar que la fecha no sea futura
    @field_validator("fecha_venta", mode='before')
    @classmethod
    def validate_fecha_venta_not_future(cls, v):
        """Asegura que la fecha de venta no sea en el futuro."""
        if v and v > datetime.now():
            raise ValueError("La fecha de venta no puede ser en el futuro.")
        return v

# Venta: Modelo de tabla ORM
class Venta(VentaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Relación de vuelta al Auto (Many-to-One)
    auto: Optional["Auto"] = Relationship(back_populates="ventas")

# VentaResponse: Modelo para respuestas de API (incluye ID)
class VentaResponse(VentaBase):
    id: int

# VentaCreate: Modelo para la creación de nuevos registros
class VentaCreate(VentaBase):
    pass

# VentaUpdate: Modelo para actualizaciones parciales (todos los campos opcionales)
class VentaUpdate(SQLModel):
    nombre_comprador: Optional[str] = Field(default=None, min_length=1)
    precio: Optional[float] = Field(default=None, gt=0)
    fecha_venta: Optional[datetime] = Field(default=None)
    auto_id: Optional[int] = Field(default=None, foreign_key="auto.id")

    # Reutilizamos la lógica del validador para la actualización
    @field_validator("fecha_venta", mode='before')
    @classmethod
    def validate_fecha_venta_not_future_update(cls, v):
        if v and v > datetime.now():
            raise ValueError("La fecha de venta no puede ser en el futuro.")
        return v


# ====================================================================
# --- 2. Modelos de Auto (One side) ---
# ====================================================================

# AutoBase: Campos comunes con validaciones Pydantic
class AutoBase(SQLModel):
    marca: str
    modelo: str
    # Validación: Único en la base de datos
    numero_chasis: str = Field(unique=True, index=True)
    # Validación: Año entre 1900 y año actual
    año: int = Field(ge=1900, le=CURRENT_YEAR)

    # Validador para numero_chasis (alfanumérico)
    @field_validator("numero_chasis", mode='before')
    @classmethod
    def validate_chasis_alphanumeric(cls, v):
        """Asegura que el número de chasis sea estrictamente alfanumérico (letras o números)."""
        if not isinstance(v, str) or not re.fullmatch(r"^[a-zA-Z0-9]+$", v):
            raise ValueError("El número de chasis debe ser estrictamente alfanumérico (sin espacios ni símbolos).")
        return v

# Auto: Modelo de tabla ORM
class Auto(AutoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Relación One-to-Many con Venta
    ventas: List[Venta] = Relationship(back_populates="auto")

# AutoResponse: Modelo para respuestas de API (incluye ID)
class AutoResponse(AutoBase):
    id: int

# AutoCreate: Modelo para la creación de nuevos registros
class AutoCreate(AutoBase):
    pass

# AutoUpdate: Modelo para actualizaciones parciales (todos los campos opcionales)
class AutoUpdate(SQLModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    numero_chasis: Optional[str] = Field(default=None, unique=True, index=True)
    año: Optional[int] = Field(default=None, ge=1900, le=CURRENT_YEAR)

    # Reutilizamos la lógica del validador para el chasis en la actualización
    @field_validator("numero_chasis", mode='before')
    @classmethod
    def validate_chasis_alphanumeric_update(cls, v):
        if v and not re.fullmatch(r"^[a-zA-Z0-9]+$", v):
            raise ValueError("El número de chasis debe ser estrictamente alfanumérico (sin espacios ni símbolos).")
        return v


# ====================================================================
# --- 3. Modelos de Respuesta con Relaciones Anidadas ---
# ====================================================================

# AutoResponseWithVentas: Incluye la lista de ventas asociadas
class AutoResponseWithVentas(AutoResponse):
    ventas: List[VentaResponse] = [] # Usamos VentaResponse para la anidación

# VentaResponseWithAuto: Incluye la información del Auto asociado
class VentaResponseWithAuto(VentaResponse):
    auto: Optional[AutoResponse] = None # Usamos AutoResponse para la anidación