from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session

from database import get_session
from repository import AutoRepository, VentaRepository
from models import (
    VentaCreate,
    VentaResponse,
    VentaResponseWithAuto,
    VentaUpdate,
    AutoResponse
)

# -------------------------------------------------------------------
# Configuración del Router y Dependencias
# -------------------------------------------------------------------

router = APIRouter(prefix="/ventas", tags=["Ventas"])

def get_auto_repository(session: Session = Depends(get_session)) -> AutoRepository:
    """Provee una instancia del AutoRepository."""
    return AutoRepository(session)

def get_venta_repository(session: Session = Depends(get_session)) -> VentaRepository:
    """Provee una instancia del VentaRepository."""
    return VentaRepository(session)

# -------------------------------------------------------------------
# 1. POST /ventas - Crear nueva venta
# -------------------------------------------------------------------

@router.post("/", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def create_venta(
    venta_data: VentaCreate,
    venta_repo: VentaRepository = Depends(get_venta_repository),
    auto_repo: AutoRepository = Depends(get_auto_repository)
):
    """
    Crea una nueva Venta, verificando que el auto asociado (auto_id) exista.
    """
    # Verificación de la clave foránea
    if not auto_repo.get_by_id(venta_data.auto_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto con ID {venta_data.auto_id} no encontrado. No se puede crear la venta."
        )
    
    try:
        new_venta = venta_repo.create(venta_data)
        return new_venta
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear la venta: {e}"
        )

# -------------------------------------------------------------------
# 2. GET /ventas - Listar ventas con paginación
# -------------------------------------------------------------------

@router.get("/", response_model=List[VentaResponse])
def read_all_ventas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0, le=100),
    repository: VentaRepository = Depends(get_venta_repository)
):
    """
    Obtiene la lista de todas las Ventas registradas con paginación.
    """
    return repository.get_all(skip=skip, limit=limit)

# -------------------------------------------------------------------
# 3. GET /ventas/{venta_id} - Obtener venta por ID (Respuesta simple)
# -------------------------------------------------------------------

@router.get("/{venta_id}", response_model=VentaResponse)
def read_venta_by_id_simple(
    venta_id: int,
    repository: VentaRepository = Depends(get_venta_repository)
):
    """
    Obtiene una Venta específica por su ID.
    """
    venta = repository.get_by_id(venta_id)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venta con ID {venta_id} no encontrada"
        )
    return venta

# -------------------------------------------------------------------
# 4. PUT /ventas/{venta_id} - Actualizar venta (Reemplazo total)
# -------------------------------------------------------------------
# Nota: Usamos VentaCreate para el PUT para asegurar que se envíen todos los campos
@router.put("/{venta_id}", response_model=VentaResponse)
def replace_venta(
    venta_id: int,
    venta_data: VentaCreate,
    venta_repo: VentaRepository = Depends(get_venta_repository),
    auto_repo: AutoRepository = Depends(get_auto_repository)
):
    """
    Actualiza completamente una Venta por su ID (PUT). Requiere todos los campos.
    """
    # 1. Verificar si el nuevo auto_id existe (si se está cambiando)
    if not auto_repo.get_by_id(venta_data.auto_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto con ID {venta_data.auto_id} no encontrado. No se puede actualizar la venta."
        )

    # 2. Convertir a VentaUpdate y realizar la actualización
    venta_update_data = VentaUpdate.model_validate(venta_data.model_dump())
    updated_venta = venta_repo.update(venta_id, venta_update_data)
    
    if not updated_venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venta con ID {venta_id} no encontrada"
        )
    return updated_venta

# -------------------------------------------------------------------
# 5. DELETE /ventas/{venta_id} - Eliminar venta
# -------------------------------------------------------------------

@router.delete("/{venta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_venta(
    venta_id: int,
    repository: VentaRepository = Depends(get_venta_repository)
):
    """
    Elimina una Venta por su ID.
    """
    success = repository.delete(venta_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venta con ID {venta_id} no encontrada"
        )
    return 

# -------------------------------------------------------------------
# 6. GET /ventas/auto/{auto_id} - Ventas de un auto específico
# -------------------------------------------------------------------

@router.get("/auto/{auto_id}", response_model=List[VentaResponse])
def read_ventas_by_auto_id(
    auto_id: int,
    venta_repo: VentaRepository = Depends(get_venta_repository),
    auto_repo: AutoRepository = Depends(get_auto_repository)
):
    """
    Obtiene todas las Ventas asociadas a un Auto específico.
    """
    # 1. Verificar si el Auto existe antes de buscar sus ventas
    if not auto_repo.get_by_id(auto_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto con ID {auto_id} no encontrado"
        )
        
    ventas = venta_repo.get_by_auto_id(auto_id)
    return ventas

# -------------------------------------------------------------------
# 7. GET /ventas/comprador/{nombre} - Ventas por nombre de comprador
# -------------------------------------------------------------------
# Nota: La ruta debe ser específica para evitar conflictos con /{venta_id}
@router.get("/comprador/{nombre}", response_model=List[VentaResponse])
def read_ventas_by_comprador(
    nombre: str,
    repository: VentaRepository = Depends(get_venta_repository)
):
    """
    Busca Ventas cuyo nombre de comprador contenga el texto especificado.
    """
    ventas = repository.get_by_comprador(nombre)
    return ventas

# -------------------------------------------------------------------
# 8. GET /ventas/{venta_id}/with-auto - Venta con información del auto
# -------------------------------------------------------------------

@router.get("/{venta_id}/with-auto", response_model=VentaResponseWithAuto)
def read_venta_with_auto(
    venta_id: int,
    repository: VentaRepository = Depends(get_venta_repository)
):
    """
    Obtiene una Venta específica por su ID, incluyendo los detalles del Auto vendido.
    """
    venta = repository.get_by_id(venta_id)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venta con ID {venta_id} no encontrada"
        )
    # Gracias a la relación definida en models.py, 'venta' ya incluye el objeto 'auto'.
    return venta