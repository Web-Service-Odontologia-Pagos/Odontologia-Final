class FacturaDB(Base):
    """
    Tabla de Facturas. Esencial para HU-22 (filtro 'Pendiente') y HU-21 (validación).
    """
    __tablename__ = "facturas"
    id = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    id_tratamiento = Column(Integer, ForeignKey("tratamientos.id"), nullable=False)
    monto_total = Column(Float, nullable=False)
    monto_pendiente = Column(Float, nullable=False)
    estado_factura = Column(Enum("Pendiente", "Pagada", "Cancelada", name="estado_factura_enum"),
                            default="Pendiente", nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now)