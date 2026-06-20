from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EstadiaBase(BaseModel):
    hotel_id: str
    reserva_id: str
    habitacion_id: str
    huesped_id: str
    deposito_garantia: float = 0.00
    creado_por: Optional[str] = None


class EstadiaCreate(EstadiaBase):
    pass


class EstadiaResponse(EstadiaBase):
    id: str
    fecha_checkin_real: datetime
    fecha_checkout_real: Optional[datetime] = None
    calificacion: Optional[int] = None
    creado_en: datetime


class CheckinDocumentoVerificadoCreate(BaseModel):
    estadia_id: str
    huesped_id: str
    tipo_documento: str
    numero_documento: str
    verificado_por: Optional[str] = None


class CheckinDocumentoVerificadoResponse(BaseModel):
    id: str
    estadia_id: str
    huesped_id: str
    tipo_documento: str
    numero_documento: str
    verificado_por: Optional[str] = None
    verificado_en: datetime
