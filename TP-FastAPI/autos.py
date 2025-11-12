from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session

from database import get_session
from repository import AutoRepository
from models import (
    AutoCreate,
    AutoResponse,
    AutoResponseWithVentas,
    AutoUpdate,
)

# -------------------------------------------------------------------
# Configuración del Router y Dependencia del Repositorio
# -------------------------------------------------------------------

router = APIRouter(prefix="/autos", tags=["Autos"])

def get_auto_repository(session: Session = Depends(get_session)) -> AutoRepository:
    """Provee una instancia del AutoRepository con una sesión activa."""
    return AutoRepository(session)

# -------------------------------------------------------------------
# 1. POST /autos - Crear nuevo auto
# -------------------------------------------------------------------

@router.post("/", response_model=AutoResponse, status_code=status.HTTP_201_CREATED)
def create_auto(
    auto_data: AutoCreate,
    repository: AutoRepository = Depends(get_auto_repository)
):
    """
    Crea un nuevo Auto en la base de datos.
    """
    try:
        new_auto = repository.create(auto_data)
        return new_auto
    except Exception as e:
        # Esto puede capturar errores de unicidad (chasis duplicado)
        # o fallos de validación del ORM.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear el auto (Verifique chasis único): {e}"
        )

# -------------------------------------------------------------------
# 2. GET /autos - Listar autos con paginación
# -------------------------------------------------------------------

@router.get("/", response_model=List[AutoResponse])
def read_all_autos(
    skip: int = Query(0, ge=0), # Paginación: Índice de inicio
    limit: int = Query(100, gt=0, le=100), # Paginación: Cantidad de registros
    repository: AutoRepository = Depends(get_auto_repository)
):
    """
    Obtiene la lista de todos los Autos registrados con paginación.
    """
    return repository.get_all(skip=skip, limit=limit)

# -------------------------------------------------------------------
# 3. GET /autos/{auto_id} - Obtener auto por ID (Respuesta simple)
# -------------------------------------------------------------------

@router.get("/{auto_id}", response_model=AutoResponse)
def read_auto_by_id_simple(
    auto_id: int,
    repository: AutoRepository = Depends(get_auto_repository)
):
    """
    Obtiene un Auto específico por su ID.
    """
    auto = repository.get_by_id(auto_id)
    if not auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto con ID {auto_id} no encontrado"
        )
    return auto

# -------------------------------------------------------------------
# 4. PUT /autos/{auto_id} - Actualizar auto (Reemplazo total)
# -------------------------------------------------------------------
# Nota: La funcionalidad PATCH que habíamos hecho es más común para updates parciales.
# Para un PUT estricto (reemplazo total), se usaría AutoCreate en la entrada
# y se requeriría que todos los campos sean enviados. Usaremos el método update
# del repositorio para manejarlo, asumiendo que el cliente enviará todos los datos.

@router.put("/{auto_id}", response_model=AutoResponse)
def replace_auto(
    auto_id: int,
    auto_data: AutoCreate, # Usamos AutoCreate para asegurar que se envíen todos los campos
    repository: AutoRepository = Depends(get_auto_repository)
):
    """
    Actualiza completamente un Auto por su ID (PUT). Requiere todos los campos.
    """
    # Convertimos AutoCreate a AutoUpdate para usar el método update del repositorio
    auto_update_data = AutoUpdate.model_validate(auto_data.model_dump())
    
    updated_auto = repository.update(auto_id, auto_update_data)
    
    if not updated_auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto con ID {auto_id} no encontrado"
        )
    return updated_auto

# -------------------------------------------------------------------
# 5. DELETE /autos/{auto_id} - Eliminar auto
# -------------------------------------------------------------------

@router.delete("/{auto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_auto(
    auto_id: int,
    repository: AutoRepository = Depends(get_auto_repository)
):
    """
    Elimina un Auto por su ID.
    """
    success = repository.delete(auto_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto con ID {auto_id} no encontrado"
        )
    return 

# -------------------------------------------------------------------
# 6. GET /autos/chasis/{numero_chasis} - Buscar por número de chasis
# -------------------------------------------------------------------
# Nota: La ruta debe ser específica para evitar conflictos con /{auto_id}
@router.get("/chasis/{numero_chasis}", response_model=AutoResponse)
def read_auto_by_chasis(
    numero_chasis: str,
    repository: AutoRepository = Depends(get_auto_repository)
):
    """
    Busca un Auto por su número de chasis único.
    """
    auto = repository.get_by_chasis(numero_chasis)
    if not auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto con chasis {numero_chasis} no encontrado"
        )
    return auto

# -------------------------------------------------------------------
# 7. GET /autos/{auto_id}/with-ventas - Auto con sus ventas
# -------------------------------------------------------------------
# Esta ruta utiliza una ruta anidada para ser más clara y evitar la colisión
# con la ruta simple GET /{auto_id}.

@router.get("/{auto_id}/with-ventas", response_model=AutoResponseWithVentas)
def read_auto_with_ventas(
    auto_id: int,
    repository: AutoRepository = Depends(get_auto_repository)
):
    """
    Obtiene un Auto específico por su ID, incluyendo el historial de Ventas asociadas.
    """
    auto = repository.get_by_id(auto_id)
    if not auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto con ID {auto_id} no encontrado"
        )
    # Gracias a la relación definida en models.py, 'auto' ya incluye la lista de 'ventas'.
    return auto