from typing import Optional, List
from datetime import datetime
import re
from sqlmodel import SQLModel, Field, Relationship

#Año actual
def current_year() -> int:
    return datetime.now().year

#AUTOS

# Base Model
class AutoBase(SQLModel):
    marca: str = Field(max_length=50)
    modelo: str = Field(max_length=50)
    año: int = Field(ge=1900, le=2025)
    color: str = Field(max_length=30)
    precio: float = Field(ge=0)
    numero_chasis: str = Field(
        max_length=17,
        min_length=10,
        unique=True,
        index=True,
        description="Debe ser alfanumerico (letras y numeros)" 
    )
    
    #Validation
    @classmethod
    def validate_chasis(cls, v: str) -> str:
        if not re.match("^[a-zA-Z0-9]+$", v):
            raise ValueError("El numero de chasis debe ser alfanumerico (letras y numeros)")
        return v
    
    from pydantic import field_validator
    _validate_chasis = field_validator('numero_chasis')(validate_chasis)

# Table Model with Relations
class Auto(AutoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relacion con Venta (One To Many)
    ventas: List["Venta"] = Relationship(back_populates="auto")
    
# Create Model (NO ID)
class AutoCreate(AutoBase):
    pass

#Update Model
class AutoUpdate(SQLModel):
    marca: Optional[str] = Field(default=None, max_length=50)
    modelo: Optional[str] = Field(default=None, max_length=50)
    año: Optional[int] = Field(default=None, ge=1900, le=2025)
    color: Optional[str] = Field(dafult=None, max_length=30)
    precio: Optional[float] = Field(dafult=None, ge=0)
    numero_chasis: Optional[str] = Field(
        default=None,
        max_length=17,
        min_length=10,
        description="Debe ser alfanumerico"
    )
    
    @field_validator('numero_chasis', mode='before')
    @classmethod
    def validate_chasis_update(cls, v):
        if v is not None:
            if not re.match("^[a-zA-Z0-9]+$", v):
                raise ValueError("El numero de chasis debe ser alfanumerico")
            return v
    
    
#Response Model NO Relation
class AutoResponse(AutoBase):
    id: int
    
#Reponse Model with ventas
class AutoResponseWithVentas(AutoResponse):
    ventas: List["VentaResponse"] = []
    
    
# VENTAS

# Base Model
class VentaBase(SQLModel):
    fecha: datetime
    comprador: str = Field(max_length=100)
    monto: float = Field(ge=0)
    auto_id: int = Field(foreign_key="auto.id") #Relation with Auto
    
    @field_validator('comprador')
    @classmethod
    def validate_comprador_no_vacio(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre del comprador no puede estar vacio")
        return v.strip()
    
    @field_validator('fecha')
    @classmethod
    def validate_fecha_no_futura(cls, v: datetime) -> datetime:
        if v > datetime.now():
            raise ValueError("La fecha de venta no puede ser futura")
        return v
    
# Table Model with Relations
class Venta(VentaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    #Inverse Relation with Auto
    auto: "Auto" = Relationship(back_populates="ventas")
    
# Create Model (NO ID)
class VentaCreate(VentaBase):
    pass

#Update Model
class VentaUpdate(SQLModel):
    fecha: Optional[datetime] = None
    comprador: Optional[str] = Field(default=None, max_length=100)
    monto: Optional[float] = Field(default=None, ge=0)
    auto_id: Optional[int] = Field(default=None, foreign_key="auto.id")
    
    @field_validator('comprador', mode='before')
    @classmethod
    def validate_comprador_update(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError("EL nombre del comprador no puede estar vacio")
            return v
    
    @field_validator('fecha', mode='before')
    @classmethod
    def validate_fecha_update(cls, v):
        if v is not None:
            if v > datetime.now():
                raise ValueError("La fecha de venta no puede ser futura")
        return v
    
# Response Model API (NO Relations)
class VentaResponse(VentaBase):
    id: int
    
#Reponse Model with Auto Information
class VentaResponseWithAuto(VentaResponse):
    auto: "AutoResponse" #Basic Auto DATA 
    
AutoResponseWithVentas.update_forward_refs()
VentaResponseWithAuto.update_forward_refs()