from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime, date


class DashboardHoyResponse(BaseModel):
    hotel_id: str
    hotel_nombre: str
    total_habitaciones: int
    habitaciones_libres: int
    habitaciones_ocupadas: int
    habitaciones_en_limpieza: int
    habitaciones_mantenimiento: int
    habitaciones_bloqueadas: int
    porcentaje_ocupacion: float
    llegadas_hoy: int
    salidas_hoy: int
    ingresos_hoy: float


class HabitacionRackResponse(BaseModel):
    habitacion_id: str
    hotel_id: str
    numero: str
    piso: int
    estado: str
    tipo_habitacion: str
    huesped_actual: Optional[str] = None
    fecha_salida_programada: Optional[date] = None
    estadia_id: Optional[str] = None


class ReporteOcupacionResponse(BaseModel):
    hotel_id: str
    fecha: date
    habitaciones_ocupadas: int
    total_habitaciones: int
    ingresos_alojamiento: float
    revpar: float


class ReporteIngresosResponse(BaseModel):
    hotel_id: str
    fecha: date
    categoria: str
    total: float


class HuespedInHouseResponse(BaseModel):
    hotel_id: str
    nombres: str
    apellidos: str
    tipo_documento: str
    numero_documento: str
    nacionalidad: Optional[str] = None
    habitacion: str
    fecha_checkin_real: datetime
    fecha_salida_programada: date


class HistorialHuespedResponse(BaseModel):
    huesped_id: str
    nombres: str
    apellidos: str
    estadia_id: str
    habitacion: str
    fecha_checkin_real: datetime
    fecha_checkout_real: Optional[datetime] = None
    saldo: float
    total_consumido: float


class PlanLimpiezaResponse(BaseModel):
    tarea_id: str
    hotel_id: str
    numero: str
    piso: int
    prioridad: str
    estado: str
    asignado_a_nombre: Optional[str] = None
    notas: Optional[str] = None
