from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class ReservaBase(BaseModel):
    hotel_id: str
    huesped_id: str
    tipo_habitacion_id: str
    habitacion_id: Optional[str] = None
    tarifa_id: Optional[str] = None
    fecha_llegada: date
    fecha_salida: date
    numero_huespedes: int = 1
    canal: str = "presencial"
    estado: str = "pendiente"
    politica_cancelacion_id: Optional[str] = None
    motivo_cancelacion: Optional[str] = None
    creado_por: Optional[str] = None


class ReservaCreate(ReservaBase):
    huespedes_adicionales: Optional[List[str]] = None


class ReservaUpdate(BaseModel):
    tipo_habitacion_id: Optional[str] = None
    habitacion_id: Optional[str] = None
    tarifa_id: Optional[str] = None
    fecha_llegada: Optional[date] = None
    fecha_salida: Optional[date] = None
    numero_huespedes: Optional[int] = None
    canal: Optional[str] = None
    estado: Optional[str] = None
    politica_cancelacion_id: Optional[str] = None
    motivo_cancelacion: Optional[str] = None


class ReservaResponse(ReservaBase):
    id: str
    codigo_reserva: str
    creado_en: datetime
    actualizado_en: datetime


class ReservaHuespedAdicionalCreate(BaseModel):
    reserva_id: str
    huesped_id: str


class ReservaHuespedAdicionalResponse(BaseModel):
    id: str
    reserva_id: str
    huesped_id: str
