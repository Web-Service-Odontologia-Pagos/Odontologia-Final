# app/domain/paciente_model.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class PacienteBase(BaseModel):
    """Modelo base con datos que no cambian a menudo."""
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None

class PacienteResponse(PacienteBase):
    """Modelo para MOSTRAR la información del paciente."""
    id: int

    class Config:
        from_attributes = True