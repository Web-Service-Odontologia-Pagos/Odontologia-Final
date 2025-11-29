class PagoDB(Base):
    """
    Tabla de Pagos. Clave para HU-21 (inicio) y HU-26 (actualización atómica).
    """
    __tablename__ = "pagos"
    id = Column(Integer, primary_key=True, index=True)
    id_factura = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    id_transaccion_banco = Column(String(50), unique=True, nullable=True)
    monto_pagado = Column(Float, nullable=False)
    estado_pago = Column(Enum("En Proceso", "Pagado", "Rechazado", name="estado_pago_enum"),
                         default="En Proceso", nullable=False)
    fecha_inicio = Column(DateTime, default=datetime.now)
    fecha_finalizacion = Column(DateTime, nullable=True)