from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class HuespedBase(BaseModel):
    hotel_id: str
    nombres: str
    apellidos: str
    tipo_documento: str
    numero_documento: str
    nacionalidad: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    es_vip: bool = False
    notas: Optional[str] = None


class HuespedCreate(HuespedBase):
    pass


class HuespedUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    tipo_documento: Optional[str] = None
    numero_documento: Optional[str] = None
    nacionalidad: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    es_vip: Optional[bool] = None
    notas: Optional[str] = None


class HuespedResponse(HuespedBase):
    id: str
    creado_en: datetime
    actualizado_en: datetime
