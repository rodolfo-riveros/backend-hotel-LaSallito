from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class TareaLimpiezaBase(BaseModel):
    hotel_id: str
    habitacion_id: str
    fecha: date
    prioridad: str
    estado: str = "pendiente"
    asignado_a: Optional[str] = None
    notas: Optional[str] = None


class TareaLimpiezaCreate(TareaLimpiezaBase):
    pass


class TareaLimpiezaUpdate(BaseModel):
    estado: Optional[str] = None
    asignado_a: Optional[str] = None
    inspeccionado_por: Optional[str] = None
    notas: Optional[str] = None


class TareaLimpiezaResponse(TareaLimpiezaBase):
    id: str
    inspeccionado_por: Optional[str] = None
    creado_en: datetime
    actualizado_en: datetime


class ObjetoPerdidoBase(BaseModel):
    hotel_id: str
    habitacion_id: Optional[str] = None
    descripcion: str
    ubicacion: Optional[str] = None
    encontrado_por: Optional[str] = None
    notas: Optional[str] = None


class ObjetoPerdidoCreate(ObjetoPerdidoBase):
    pass


class ObjetoPerdidoUpdate(BaseModel):
    entregado: Optional[bool] = None
    notas: Optional[str] = None


class ObjetoPerdidoResponse(ObjetoPerdidoBase):
    id: str
    encontrado_en: datetime
    entregado: bool
    entregado_en: Optional[datetime] = None
