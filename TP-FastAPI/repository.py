from datetime import datetime
from typing import List, Optional

from sqlmodel import Session, or_, select

from models import (
    Auto,
    AutoCreate,
    AutoUpdate,
    Venta,
    VentaCreate,
    VentaUpdate
)


class AutoRepository:
    """
    Clase Repository para manejar las operaciones CRUD y búsquedas de la entidad Auto.
    """
    def __init__(self, session: Session):
        """Inicializa el repositorio con la sesión de la base de datos."""
        self.session = session

    # Crear
    def create(self, auto_data: AutoCreate) -> Auto:
        """Crea un nuevo Auto en la base de datos."""
        db_auto = Auto.model_validate(auto_data)
        self.session.add(db_auto)
        self.session.commit()
        self.session.refresh(db_auto)
        return db_auto

    # Obtener por ID
    def get_by_id(self, auto_id: int) -> Optional[Auto]:
        """Obtiene un Auto por su ID."""
        auto = self.session.get(Auto, auto_id)
        return auto

    # Obtener todos con paginación
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Auto]:
        """Obtiene una lista de Autos con paginación (skip y limit)."""
        # Añadimos .offset(skip) y .limit(limit) para la paginación
        statement = select(Auto).offset(skip).limit(limit)
        autos = self.session.exec(statement).all()
        return autos

    # Actualizar
    def update(self, auto_id: int, auto_data: AutoUpdate) -> Optional[Auto]:
        """Actualiza parcialmente un Auto (PATCH/PUT)."""
        db_auto = self.session.get(Auto, auto_id)
        if not db_auto:
            return None

        # Obtiene los campos enviados por el cliente que no son None
        update_data = auto_data.model_dump(exclude_unset=True)
    
        # Itera sobre los campos y valores que deben ser actualizados
        for key, value in update_data.items():
            # Aplica el nuevo valor al objeto de la base de datos
            setattr(db_auto, key, value)
    
        # NO es necesario usar model_validate aquí si usamos setattr
        # La validación ocurrirá automáticamente al hacer db_auto = self.session.add(db_auto)
    
        self.session.add(db_auto)
        self.session.commit()
        self.session.refresh(db_auto)
        return db_auto

    # Eliminar
    def delete(self, auto_id: int) -> bool:
        """Elimina un Auto por su ID."""
        auto = self.session.get(Auto, auto_id)
        if auto:
            self.session.delete(auto)
            self.session.commit()
            return True
        return False
    
    # Búsqueda específica
    def get_by_chasis(self, numero_chasis: str) -> Optional[Auto]:
        """Obtiene un Auto por su número de chasis único."""
        statement = select(Auto).where(Auto.numero_chasis == numero_chasis)
        auto = self.session.exec(statement).first()
        return auto
    
    # Búsqueda por Marca o Modelo
    def search_by_brand_or_model(self, query: str, skip: int = 0, limit: int = 100) -> List[Auto]:
        """
        Busca autos donde la marca o el modelo contengan la cadena de consulta.
        """
        search_term = f"%{query}%"
        
        statement = (
            select(Auto)
            .where(
                or_(
                    Auto.marca.ilike(search_term),  # ilike es case-insensitive LIKE
                    Auto.modelo.ilike(search_term)
                )
            )
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(statement).all()


class VentaRepository:
    """
    Clase Repository para manejar las operaciones CRUD y búsquedas de la entidad Venta.
    """
    def __init__(self, session: Session):
        self.session = session

    # Crear
    def create(self, venta_data: VentaCreate) -> Venta:
        """Crea una nueva Venta en la base de datos."""
        db_venta = Venta.model_validate(venta_data)
        self.session.add(db_venta)
        self.session.commit()
        self.session.refresh(db_venta)
        return db_venta

    # Obtener por ID
    def get_by_id(self, venta_id: int) -> Optional[Venta]:
        """Obtiene una Venta por su ID."""
        venta = self.session.get(Venta, venta_id)
        return venta

    # Obtener todos con paginación
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Venta]:
        """Obtiene una lista de Ventas con paginación (skip y limit)."""
        statement = select(Venta).offset(skip).limit(limit)
        ventas = self.session.exec(statement).all()
        return ventas

    # Actualizar
    def update(self, venta_id: int, venta_data: VentaUpdate) -> Optional[Venta]:
        """Actualiza parcialmente una Venta (PATCH/PUT) usando setattr."""
        db_venta = self.session.get(Venta, venta_id)
        if not db_venta:
            return None

        # Obtiene los campos enviados por el cliente que no son None
        update_data = venta_data.model_dump(exclude_unset=True)
    
        # Itera y aplica los nuevos valores al objeto de la base de datos
        for key, value in update_data.items():
            setattr(db_venta, key, value)
    
        self.session.add(db_venta)
        self.session.commit()
        self.session.refresh(db_venta)
        return db_venta

    # Eliminar
    def delete(self, venta_id: int) -> bool:
        """Elimina una Venta por su ID."""
        venta = self.session.get(Venta, venta_id)
        if venta:
            self.session.delete(venta)
            self.session.commit()
            return True
        return False

    # Búsqueda específica por Auto ID
    def get_by_auto_id(self, auto_id: int) -> List[Venta]:
        """Obtiene todas las Ventas asociadas a un Auto específico."""
        statement = select(Venta).where(Venta.auto_id == auto_id)
        ventas = self.session.exec(statement).all()
        return ventas

    # Búsqueda específica por Comprador
    def get_by_comprador(self, nombre: str) -> List[Venta]:
        """
        Obtiene Ventas por el nombre del comprador (búsqueda parcial con LIKE).
        """
        # Usamos .contains() para un LIKE %nombre% en la base de datos
        statement = select(Venta).where(Venta.nombre_comprador.contains(nombre))
        ventas = self.session.exec(statement).all()
        return ventas
    
    # Filtrado por Rango de Precios
    def filter_by_price_range(self, min_price: float, max_price: float, skip: int = 0, limit: int = 100) -> List[Venta]:
        """
        Obtiene ventas dentro de un rango de precios (mínimo y máximo).
        """
        statement = (
            select(Venta)
            .where(Venta.precio >= min_price, Venta.precio <= max_price)
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(statement).all()

    # Filtrado por Rango de Fechas
    def filter_by_date_range(self, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100) -> List[Venta]:
        """
        Obtiene ventas realizadas entre dos fechas específicas (rango inclusivo).
        """
        statement = (
            select(Venta)
            .where(Venta.fecha_venta >= start_date, Venta.fecha_venta <= end_date)
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(statement).all()