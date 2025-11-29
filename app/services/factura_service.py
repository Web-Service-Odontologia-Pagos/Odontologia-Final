# app/services/factura_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository.factura_repository import FacturaRepository
from app.repository.paciente_repository import PacienteRepository
from app.domain.factura_model import (
    FacturaResponse,
    ConsultaFacturasResponse,
    ConsultaSaldosData,
    DetalleFactura
)
from datetime import date
from typing import List, Optional


class FacturaService:
    """
    Capa de servicios para lógica de negocio de Facturas.
    Maneja validaciones, orquestación de repositorios y transformaciones de datos.
    """

    def __init__(self, db: Session):
        """
        Constructor que inicializa los repositorios necesarios.
        
        Args:
            db (Session): Sesión SQLAlchemy activa
        """
        self.factura_repo = FacturaRepository(db)
        self.paciente_repo = PacienteRepository(db)
        self.db = db
    
    # ========================================================================
    # HU-22: CONSULTA DE FACTURAS PENDIENTES (ConsultaF)
    # ========================================================================

    def get_facturas_pendientes_by_paciente(self, paciente_id: int) -> List[FacturaResponse]:
        """
        [HU-22: ConsultaF] - Obtiene lista simple de facturas pendientes.
        
        Validaciones:
        1. Verificar que el paciente exista
        2. Filtrar solo facturas en estado "Pendiente"
        
        Args:
            paciente_id (int): ID del paciente a consultar
            
        Returns:
            List[FacturaResponse]: Lista de facturas pendientes
            
        Raises:
            HTTPException: 404 si el paciente no existe
        """
        # Validación de Negocio: Verificar que el paciente existe
        paciente = self.paciente_repo.get_paciente_by_id(paciente_id)
        
        if not paciente:
            raise HTTPException(
                status_code=404, 
                detail=f"Paciente con ID {paciente_id} no encontrado."
            )
            
        # Orquestación: Obtener facturas pendientes
        facturas_db = self.factura_repo.get_facturas_pendientes_by_paciente(paciente_id)
        
        # Mapeo: Convertir FacturaDB a FacturaResponse
        return [FacturaResponse.model_validate(factura) for factura in facturas_db]

    def consultar_saldos_paciente(
        self,
        paciente_id: int,
        intereses_causados: float = 0.0,
        intereses_contingentes: float = 0.0
    ) -> ConsultaFacturasResponse:
        """
        [HU-22: ConsultaF] - Respuesta COMPLETA con estructura de saldos.
        
        Retorna la respuesta estructurada con:
        - Fecha de proceso
        - Capital total adeudado
        - Intereses opcionales
        - Detalle de cada factura
        
        Args:
            paciente_id (int): ID del paciente
            intereses_causados (float): Intereses por mora (opcional)
            intereses_contingentes (float): Intereses contingentes (opcional)
            
        Returns:
            ConsultaFacturasResponse: Respuesta completa con saldos y detalles
            
        Raises:
            HTTPException: 404 si el paciente no existe
        """
        # Validación: Verificar que el paciente existe
        paciente = self.paciente_repo.get_paciente_by_id(paciente_id)
        
        if not paciente:
            raise HTTPException(
                status_code=404, 
                detail=f"Paciente con ID {paciente_id} no encontrado."
            )
        
        # Obtener facturas pendientes
        facturas_db = self.factura_repo.get_facturas_pendientes_by_paciente(paciente_id)
        
        # Si no hay facturas pendientes
        if not facturas_db:
            data = ConsultaSaldosData(
                fecha_proceso=date.today(),
                capital_total=0.0,
                intereses_causados=0.0,
                intereses_contingentes=0.0,
                detalle_facturas=[]
            )
            
            return ConsultaFacturasResponse(
                mensaje="No hay facturas pendientes",
                data=data,
                success=True
            )
        
        # Construir detalle de cada factura
        detalle_facturas = [
            DetalleFactura(
                id_factura=f.id,
                monto=f.monto_total,
                monto_pendiente=f.monto_pendiente,
                estado=f.estado_factura,
                fecha_creacion=f.fecha_creacion
            )
            for f in facturas_db
        ]
        
        # Calcular capital total (suma de saldos pendientes)
        capital_total = sum(f.monto_pendiente for f in facturas_db)
        
        # Construir respuesta con la estructura proporcionada
        data = ConsultaSaldosData(
            fecha_proceso=date.today(),
            capital_total=capital_total,
            intereses_causados=intereses_causados,
            intereses_contingentes=intereses_contingentes,
            detalle_facturas=detalle_facturas
        )
        
        return ConsultaFacturasResponse(
            mensaje="Consulta de saldos exitosa",
            data=data,
            success=True
        )

    # ========================================================================
    # VALIDACIONES PARA HU-21 (IPago)
    # ========================================================================

    def validar_factura_para_pago(self, factura_id: int) -> dict:
        """
        Valida que una factura sea elegible para pago (HU-21).
        
        Validaciones:
        1. La factura existe
        2. Está en estado "Pendiente"
        3. Tiene saldo pendiente > 0
        
        Args:
            factura_id (int): ID de la factura
            
        Returns:
            dict: {"valida": bool, "error": str o None}
        """
        # Validar existencia
        factura = self.factura_repo.get_factura_by_id(factura_id)
        if not factura:
            return {"valida": False, "error": f"Factura {factura_id} no existe"}
        
        # Validar estado
        if factura.estado_factura != "Pendiente":
            return {
                "valida": False, 
                "error": f"Factura {factura_id} no está pendiente (estado: {factura.estado_factura})"
            }
        
        # Validar saldo
        if factura.monto_pendiente <= 0:
            return {
                "valida": False,
                "error": f"Factura {factura_id} no tiene saldo pendiente"
            }
        
        return {"valida": True, "error": None}

    # ========================================================================
    # OPERACIONES DE PAGO (HU-26: CambioEP)
    # ========================================================================

    def procesar_pago_exitoso(
        self,
        factura_id: int,
        monto_pagado: float,
        id_transaccion_banco: str
    ) -> FacturaResponse:
        """
        Procesa un pago exitoso recibido del banco (HU-26).
        
        Args:
            factura_id (int): ID de la factura
            monto_pagado (float): Monto pagado
            id_transaccion_banco (str): ID de referencia del banco
            
        Returns:
            FacturaResponse: Factura actualizada
            
        Raises:
            HTTPException: Si hay validaciones fallidas
        """
        # Validar factura
        validacion = self.validar_factura_para_pago(factura_id)
        if not validacion["valida"]:
            raise HTTPException(status_code=400, detail=validacion["error"])
        
        # Actualizar saldo
        factura_actualizada = self.factura_repo.actualizar_saldo_pendiente(
            factura_id,
            monto_pagado
        )
        
        if factura_actualizada is None:
            raise HTTPException(
                status_code=500,
                detail=f"No se pudo actualizar factura {factura_id}"
            )
        
        return FacturaResponse.model_validate(factura_actualizada)

    def procesar_pago_rechazado(self, factura_id: int, motivo: str = "") -> FacturaResponse:
        """
        Procesa un pago rechazado del banco (HU-26).
        La factura permanece como pendiente.
        
        Args:
            factura_id (int): ID de la factura
            motivo (str): Motivo del rechazo (para logging)
            
        Returns:
            FacturaResponse: Factura (sin cambios)
            
        Raises:
            HTTPException: Si la factura no existe
        """
        factura = self.factura_repo.get_factura_by_id(factura_id)
        
        if not factura:
            raise HTTPException(status_code=404, detail=f"Factura {factura_id} no encontrada")
        
        # TODO: Registrar rechazo en logs
        # logger.warning(f"Pago rechazado: Factura {factura_id} - {motivo}")
        
        return FacturaResponse.model_validate(factura)

    # ========================================================================
    # ANÁLISIS Y REPORTES
    # ========================================================================

    def get_resumen_paciente(self, paciente_id: int) -> dict:
        """
        Retorna un resumen financiero completo del paciente.
        
        Args:
            paciente_id (int): ID del paciente
            
        Returns:
            dict: Resumen con montos y porcentajes
            
        Raises:
            HTTPException: 404 si el paciente no existe
        """
        # Validar paciente
        paciente = self.paciente_repo.get_paciente_by_id(paciente_id)
        if not paciente:
            raise HTTPException(status_code=404, detail=f"Paciente {paciente_id} no encontrado")
        
        total_facturado = self.factura_repo.get_monto_total_facturado_paciente(paciente_id)
        saldo_pendiente = self.factura_repo.get_saldo_pendiente_paciente(paciente_id)
        monto_pagado = self.factura_repo.get_monto_pagado_paciente(paciente_id)
        
        return {
            "paciente_id": paciente_id,
            "total_facturado": total_facturado,
            "total_pagado": monto_pagado,
            "total_pendiente": saldo_pendiente,
            "porcentaje_pagado": (monto_pagado / total_facturado * 100) if total_facturado > 0 else 0
        }