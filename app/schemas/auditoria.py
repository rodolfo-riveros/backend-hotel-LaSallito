from pydantic import BaseModel
from typing import Optional, Any
from datetime import date, datetime


class AuditoriaResponse(BaseModel):
    id: str
    hotel_id: Optional[str] = None
    usuario_id: Optional[str] = None
    accion: str
    tabla_afectada: str
    registro_id: Optional[str] = None
    detalle: Optional[Any] = None
    creado_en: datetime


class CierreNocturnoBase(BaseModel):
    hotel_id: str
    fecha: date
    observaciones: Optional[str] = None
    realizado_por: Optional[str] = None


class CierreNocturnoCreate(CierreNocturnoBase):
    pass


class CierreNocturnoResponse(BaseModel):
    id: str
    hotel_id: str
    fecha: date
    total_ingresos: float
    total_alojamiento: float
    total_alimentos: float
    total_servicios: float
    total_otros: float
    habitaciones_ocupadas: int
    habitaciones_disponibles: int
    porcentaje_ocupacion: float
    observaciones: Optional[str] = None
    realizado_por: Optional[str] = None
    cerrado_en: datetime
