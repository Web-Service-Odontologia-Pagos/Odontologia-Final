# app/repository/pago_repository.py

from sqlalchemy.orm import Session
from app.models.pago_db import PagoDB # Importa el modelo de la tabla Pagos
from datetime import datetime

class PagoRepository:
    """Clase que maneja las operaciones de la tabla 'pagos'."""

    def __init__(self, db: Session):
        self.db = db

    def create_pago(self, id_factura: int, monto_pagado: float) -> PagoDB:
        """
        Crea el registro de pago inicial con estado 'En Proceso' (Parte de HU-21).
        """
        pago = PagoDB(
            id_factura=id_factura,
            monto_pagado=monto_pagado,
            estado_pago="En Proceso",
            fecha_inicio=datetime.now()
        )
        self.db.add(pago)
        self.db.commit()
        self.db.refresh(pago)
        return pago

    def update_estado_pago_atomico(self, id_pago: int, estado_final: str, id_transaccion_banco: str) -> PagoDB | None:
        """
        Actualiza el estado de pago de forma atómica (HU-26: CambioEP).
        El estado final debe ser 'Pagado' o 'Rechazado'.
        """
        # 1. Consulta el registro de pago por ID
        pago = self.db.query(PagoDB).filter(PagoDB.id == id_pago).first()

        if pago:
            # 2. Actualiza los campos críticos
            pago.estado_pago = estado_final
            pago.id_transaccion_banco = id_transaccion_banco
            pago.fecha_finalizacion = datetime.now()
            
            # 3. Ejecución atómica (COMMIT)
            self.db.commit()
            self.db.refresh(pago)
            return pago
        
        return None