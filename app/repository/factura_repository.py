# app/repository/factura_repository.py

from sqlalchemy.orm import Session
from app.models.factura_db import FacturaDB
from app.models.pacientes_db import PacienteDB
from typing import List, Optional
from datetime import datetime


class FacturaRepository:
    """
    Capa de repositorio para operaciones CRUD de Facturas.
    Abstrae toda la comunicación con la base de datos.
    """
    
    def __init__(self, db: Session):
        """
        Constructor: recibe una sesión de base de datos.
        
        Args:
            db (Session): Sesión SQLAlchemy activa
        """
        self.db = db

    # ========================================================================
    # OPERACIONES CRUD BÁSICAS
    # ========================================================================

    def get_all_facturas(self) -> List[FacturaDB]:
        """
        Obtiene todas las facturas de la base de datos.
        
        Returns:
            List[FacturaDB]: Lista de todas las facturas
        """
        return self.db.query(FacturaDB).all()

    def get_factura_by_id(self, factura_id: int) -> Optional[FacturaDB]:
        """
        Busca una factura específica por su ID.
        Necesario para validación en HU-21 (verificar que factura existe).
        
        Args:
            factura_id (int): ID de la factura a obtener
            
        Returns:
            Optional[FacturaDB]: Factura encontrada o None si no existe
        """
        return self.db.query(FacturaDB).filter(FacturaDB.id == factura_id).first()

    def create_factura(
        self,
        id_paciente: int,
        id_tratamiento: int,
        monto_total: float,
        monto_pendiente: Optional[float] = None
    ) -> FacturaDB:
        """
        Crea una nueva factura en la base de datos.
        
        Args:
            id_paciente (int): ID del paciente propietario
            id_tratamiento (int): ID del tratamiento realizado
            monto_total (float): Monto total a facturar
            monto_pendiente (Optional[float]): Monto pendiente (default: igual al total)
            
        Returns:
            FacturaDB: Factura creada
            
        Raises:
            ValueError: Si monto_total <= 0
        """
        if monto_total <= 0:
            raise ValueError("El monto total debe ser mayor a 0")

        nueva_factura = FacturaDB(
            id_paciente=id_paciente,
            id_tratamiento=id_tratamiento,
            monto_total=monto_total,
            monto_pendiente=monto_pendiente or monto_total,
            estado_factura="Pendiente",
            fecha_creacion=datetime.now()
        )
        
        self.db.add(nueva_factura)
        self.db.commit()
        self.db.refresh(nueva_factura)
        
        return nueva_factura

    def update_factura(
        self,
        factura_id: int,
        **kwargs
    ) -> Optional[FacturaDB]:
        """
        Actualiza los datos de una factura.
        
        Args:
            factura_id (int): ID de la factura a actualizar
            **kwargs: Campos a actualizar (ej: monto_pendiente=500, estado_factura="Pagada")
            
        Returns:
            Optional[FacturaDB]: Factura actualizada o None si no existe
        """
        factura = self.get_factura_by_id(factura_id)
        if not factura:
            return None

        for key, value in kwargs.items():
            if hasattr(factura, key):
                setattr(factura, key, value)

        self.db.commit()
        self.db.refresh(factura)
        
        return factura

    def delete_factura(self, factura_id: int) -> bool:
        """
        Elimina una factura de la base de datos.
        
        Args:
            factura_id (int): ID de la factura a eliminar
            
        Returns:
            bool: True si se eliminó, False si no existe
        """
        factura = self.get_factura_by_id(factura_id)
        if not factura:
            return False

        self.db.delete(factura)
        self.db.commit()
        
        return True

    # ========================================================================
    # CONSULTAS ESPECIALIZADAS PARA HU-22 (ConsultaF)
    # ========================================================================

    def get_facturas_by_paciente(self, paciente_id: int) -> List[FacturaDB]:
        """
        Obtiene todas las facturas de un paciente (sin filtro de estado).
        
        Args:
            paciente_id (int): ID del paciente
            
        Returns:
            List[FacturaDB]: Lista de todas las facturas del paciente
        """
        return self.db.query(FacturaDB).filter(
            FacturaDB.id_paciente == paciente_id
        ).all()

    def get_facturas_pendientes_by_paciente(self, paciente_id: int) -> List[FacturaDB]:
        """
        Consulta todas las facturas del paciente en estado 'Pendiente'.
        **ESENCIAL PARA HU-22: ConsultaF**
        
        Args:
            paciente_id (int): ID del paciente a consultar.
        
        Returns:
            List[FacturaDB]: Lista de facturas pendientes del paciente
        """
        return (
            self.db.query(FacturaDB)
            .join(PacienteDB, FacturaDB.id_paciente == PacienteDB.id)
            .filter(
                FacturaDB.id_paciente == paciente_id,
                FacturaDB.estado_factura == "Pendiente"
            )
            .all()
        )

    def get_saldo_pendiente_paciente(self, paciente_id: int) -> float:
        """
        Calcula el saldo pendiente TOTAL de un paciente.
        Suma todos los monto_pendientes de sus facturas.
        Necesario para HU-22: ConsultaF
        
        Args:
            paciente_id (int): ID del paciente
            
        Returns:
            float: Saldo total pendiente (capital_total)
        """
        facturas = self.get_facturas_pendientes_by_paciente(paciente_id)
        return sum(f.monto_pendiente for f in facturas) if facturas else 0.0

    # ========================================================================
    # CONSULTAS POR ESTADO
    # ========================================================================

    def get_facturas_by_estado(self, estado: str) -> List[FacturaDB]:
        """
        Obtiene todas las facturas con un estado específico.
        
        Args:
            estado (str): Estado a filtrar ("Pendiente", "Pagada", "Cancelada")
            
        Returns:
            List[FacturaDB]: Lista de facturas con ese estado
        """
        return self.db.query(FacturaDB).filter(
            FacturaDB.estado_factura == estado
        ).all()

    def get_facturas_pagadas_by_paciente(self, paciente_id: int) -> List[FacturaDB]:
        """
        Obtiene todas las facturas PAGADAS de un paciente.
        
        Args:
            paciente_id (int): ID del paciente
            
        Returns:
            List[FacturaDB]: Lista de facturas pagadas
        """
        return self.db.query(FacturaDB).filter(
            FacturaDB.id_paciente == paciente_id,
            FacturaDB.estado_factura == "Pagada"
        ).all()

    # ========================================================================
    # CONSULTAS POR TRATAMIENTO
    # ========================================================================

    def get_facturas_by_tratamiento(self, tratamiento_id: int) -> List[FacturaDB]:
        """
        Obtiene todas las facturas generadas por un tratamiento específico.
        
        Args:
            tratamiento_id (int): ID del tratamiento
            
        Returns:
            List[FacturaDB]: Lista de facturas del tratamiento
        """
        return self.db.query(FacturaDB).filter(
            FacturaDB.id_tratamiento == tratamiento_id
        ).all()

    # ========================================================================
    # OPERACIONES DE PAGO Y ESTADO
    # ========================================================================

    def marcar_como_pagada(self, factura_id: int) -> Optional[FacturaDB]:
        """
        Marca una factura como PAGADA completamente.
        Usado en HU-26 después de confirmar pago del banco.
        
        Args:
            factura_id (int): ID de la factura
            
        Returns:
            Optional[FacturaDB]: Factura actualizada o None si no existe
        """
        return self.update_factura(
            factura_id,
            estado_factura="Pagada",
            monto_pendiente=0.0
        )

    def marcar_como_cancelada(self, factura_id: int) -> Optional[FacturaDB]:
        """
        Marca una factura como CANCELADA (anulada).
        
        Args:
            factura_id (int): ID de la factura
            
        Returns:
            Optional[FacturaDB]: Factura actualizada o None si no existe
        """
        return self.update_factura(
            factura_id,
            estado_factura="Cancelada"
        )

    def actualizar_saldo_pendiente(
        self,
        factura_id: int,
        monto_pagado: float
    ) -> Optional[FacturaDB]:
        """
        Actualiza el saldo pendiente de una factura después de un pago.
        Usado en HU-26 después de confirmar transacción bancaria.
        
        Valida:
        - El monto pagado sea positivo
        - El monto pagado no exceda el pendiente
        - Actualiza estado a "Pagada" si saldo llega a 0
        
        Args:
            factura_id (int): ID de la factura
            monto_pagado (float): Monto pagado en esta transacción
            
        Returns:
            Optional[FacturaDB]: Factura actualizada o None si no existe
            
        Raises:
            ValueError: Si el monto pagado es inválido
        """
        factura = self.get_factura_by_id(factura_id)
        if not factura:
            return None

        if monto_pagado < 0:
            raise ValueError("El monto pagado no puede ser negativo")

        if monto_pagado > factura.monto_pendiente:
            raise ValueError(
                f"El monto pagado ({monto_pagado}) no puede ser mayor al pendiente ({factura.monto_pendiente})"
            )

        nuevo_saldo = factura.monto_pendiente - monto_pagado
        nuevo_estado = "Pagada" if nuevo_saldo == 0 else "Pendiente"

        return self.update_factura(
            factura_id,
            monto_pendiente=nuevo_saldo,
            estado_factura=nuevo_estado
        )

    # ========================================================================
    # CÁLCULOS Y ANÁLISIS
    # ========================================================================

    def get_monto_total_facturado_paciente(self, paciente_id: int) -> float:
        """
        Calcula el monto TOTAL facturado a un paciente (sin importar estado).
        
        Args:
            paciente_id (int): ID del paciente
            
        Returns:
            float: Monto total facturado
        """
        facturas = self.get_facturas_by_paciente(paciente_id)
        return sum(f.monto_total for f in facturas) if facturas else 0.0

    def get_monto_pagado_paciente(self, paciente_id: int) -> float:
        """
        Calcula el monto PAGADO por un paciente.
        = monto_total_facturado - saldo_pendiente
        
        Args:
            paciente_id (int): ID del paciente
            
        Returns:
            float: Monto total pagado
        """
        total_facturado = self.get_monto_total_facturado_paciente(paciente_id)
        saldo_pendiente = self.get_saldo_pendiente_paciente(paciente_id)
        return total_facturado - saldo_pendiente