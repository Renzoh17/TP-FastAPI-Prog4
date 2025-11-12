from typing import List, Optional

from sqlmodel import Session, select

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

    # 1. Crear
    def create(self, auto_data: AutoCreate) -> Auto:
        """Crea un nuevo Auto en la base de datos."""
        db_auto = Auto.model_validate(auto_data)
        self.session.add(db_auto)
        self.session.commit()
        self.session.refresh(db_auto)
        return db_auto

    # 2. Obtener por ID
    def get_by_id(self, auto_id: int) -> Optional[Auto]:
        """Obtiene un Auto por su ID."""
        auto = self.session.get(Auto, auto_id)
        return auto

    # 3. Obtener todos con paginación
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Auto]:
        """Obtiene una lista de Autos con paginación (skip y limit)."""
        # Añadimos .offset(skip) y .limit(limit) para la paginación
        statement = select(Auto).offset(skip).limit(limit)
        autos = self.session.exec(statement).all()
        return autos

    # 4. Actualizar
    def update(self, auto_id: int, auto_data: AutoUpdate) -> Optional[Auto]:
        """Actualiza parcialmente un Auto (PATCH)."""
        db_auto = self.session.get(Auto, auto_id)
        if not db_auto:
            return None

        # model_dump(exclude_unset=True) obtiene solo los campos que fueron enviados
        update_data = auto_data.model_dump(exclude_unset=True)
        # model_validate(update=True) actualiza el modelo ORM
        db_auto.model_validate(update_data, update=True)
        
        self.session.add(db_auto)
        self.session.commit()
        self.session.refresh(db_auto)
        return db_auto

    # 5. Eliminar
    def delete(self, auto_id: int) -> bool:
        """Elimina un Auto por su ID."""
        auto = self.session.get(Auto, auto_id)
        if auto:
            self.session.delete(auto)
            self.session.commit()
            return True
        return False
    
    # 6. Búsqueda específica
    def get_by_chasis(self, numero_chasis: str) -> Optional[Auto]:
        """Obtiene un Auto por su número de chasis único."""
        statement = select(Auto).where(Auto.numero_chasis == numero_chasis)
        auto = self.session.exec(statement).first()
        return auto


class VentaRepository:
    """
    Clase Repository para manejar las operaciones CRUD y búsquedas de la entidad Venta.
    """
    def __init__(self, session: Session):
        self.session = session

    # 1. Crear
    def create(self, venta_data: VentaCreate) -> Venta:
        """Crea una nueva Venta en la base de datos."""
        db_venta = Venta.model_validate(venta_data)
        self.session.add(db_venta)
        self.session.commit()
        self.session.refresh(db_venta)
        return db_venta

    # 2. Obtener por ID
    def get_by_id(self, venta_id: int) -> Optional[Venta]:
        """Obtiene una Venta por su ID."""
        venta = self.session.get(Venta, venta_id)
        return venta

    # 3. Obtener todos con paginación
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Venta]:
        """Obtiene una lista de Ventas con paginación (skip y limit)."""
        statement = select(Venta).offset(skip).limit(limit)
        ventas = self.session.exec(statement).all()
        return ventas

    # 4. Actualizar
    def update(self, venta_id: int, venta_data: VentaUpdate) -> Optional[Venta]:
        """Actualiza parcialmente una Venta (PATCH)."""
        db_venta = self.session.get(Venta, venta_id)
        if not db_venta:
            return None

        update_data = venta_data.model_dump(exclude_unset=True)
        db_venta.model_validate(update_data, update=True)
        
        self.session.add(db_venta)
        self.session.commit()
        self.session.refresh(db_venta)
        return db_venta

    # 5. Eliminar
    def delete(self, venta_id: int) -> bool:
        """Elimina una Venta por su ID."""
        venta = self.session.get(Venta, venta_id)
        if venta:
            self.session.delete(venta)
            self.session.commit()
            return True
        return False

    # 6. Búsqueda específica por Auto ID
    def get_by_auto_id(self, auto_id: int) -> List[Venta]:
        """Obtiene todas las Ventas asociadas a un Auto específico."""
        statement = select(Venta).where(Venta.auto_id == auto_id)
        ventas = self.session.exec(statement).all()
        return ventas

    # 7. Búsqueda específica por Comprador
    def get_by_comprador(self, nombre: str) -> List[Venta]:
        """
        Obtiene Ventas por el nombre del comprador (búsqueda parcial con LIKE).
        """
        # Usamos .contains() para un LIKE %nombre% en la base de datos
        statement = select(Venta).where(Venta.nombre_comprador.contains(nombre))
        ventas = self.session.exec(statement).all()
        return ventas