from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time, datetime


class HotelBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    ruc: Optional[str] = None
    telefono: Optional[str] = None
    logo_url: Optional[str] = None
    hora_checkin: time = time(14, 0)
    hora_checkout: time = time(12, 0)
    porcentaje_igv: float = 18.00
    porcentaje_servicio: float = 0.00


class HotelCreate(HotelBase):
    pass


class HotelUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    ruc: Optional[str] = None
    telefono: Optional[str] = None
    logo_url: Optional[str] = None
    hora_checkin: Optional[time] = None
    hora_checkout: Optional[time] = None
    porcentaje_igv: Optional[float] = None
    porcentaje_servicio: Optional[float] = None


class HotelResponse(HotelBase):
    id: str
    creado_en: datetime
    actualizado_en: datetime


class TipoHabitacionBase(BaseModel):
    hotel_id: str
    nombre: str
    capacidad_max: int = 1
    descripcion: Optional[str] = None
    amenidades: Optional[List[str]] = None
    activo: bool = True


class TipoHabitacionCreate(TipoHabitacionBase):
    pass


class TipoHabitacionUpdate(BaseModel):
    nombre: Optional[str] = None
    capacidad_max: Optional[int] = None
    descripcion: Optional[str] = None
    amenidades: Optional[List[str]] = None
    activo: Optional[bool] = None


class TipoHabitacionResponse(TipoHabitacionBase):
    id: str
    creado_en: datetime


class HabitacionBase(BaseModel):
    hotel_id: str
    tipo_habitacion_id: str
    numero: str
    piso: int
    estado: str = "libre"
    notas: Optional[str] = None
    activo: bool = True


class HabitacionCreate(HabitacionBase):
    pass


class HabitacionUpdate(BaseModel):
    tipo_habitacion_id: Optional[str] = None
    estado: Optional[str] = None
    notas: Optional[str] = None
    activo: Optional[bool] = None


class HabitacionResponse(HabitacionBase):
    id: str
    creado_en: datetime
    actualizado_en: datetime


class TemporadaBase(BaseModel):
    hotel_id: str
    nombre: str
    fecha_inicio: date
    fecha_fin: date
    activo: bool = True


class TemporadaCreate(TemporadaBase):
    pass


class TemporadaUpdate(BaseModel):
    nombre: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    activo: Optional[bool] = None


class TemporadaResponse(TemporadaBase):
    id: str


class TarifaBase(BaseModel):
    hotel_id: str
    tipo_habitacion_id: str
    temporada_id: Optional[str] = None
    nombre: str = "Tarifa estándar"
    precio_noche: float = Field(ge=0)
    activo: bool = True


class TarifaCreate(TarifaBase):
    pass


class TarifaUpdate(BaseModel):
    temporada_id: Optional[str] = None
    nombre: Optional[str] = None
    precio_noche: Optional[float] = Field(default=None, ge=0)
    activo: Optional[bool] = None


class TarifaResponse(TarifaBase):
    id: str
    creado_en: datetime


class PoliticaCancelacionBase(BaseModel):
    hotel_id: str
    nombre: str
    descripcion: Optional[str] = None
    penalidad_porcentaje: float = 0.00
    activo: bool = True


class PoliticaCancelacionCreate(PoliticaCancelacionBase):
    pass


class PoliticaCancelacionUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    penalidad_porcentaje: Optional[float] = None
    activo: Optional[bool] = None


class PoliticaCancelacionResponse(PoliticaCancelacionBase):
    id: str
