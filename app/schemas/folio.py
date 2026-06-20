from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FolioResponse(BaseModel):
    id: str
    hotel_id: str
    estadia_id: str
    saldo: float
    abierto: bool
    creado_en: datetime
    cerrado_en: Optional[datetime] = None


class ConceptoCargoBase(BaseModel):
    hotel_id: str
    nombre: str
    afecto_igv: bool = True
    activo: bool = True


class ConceptoCargoCreate(ConceptoCargoBase):
    pass


class ConceptoCargoUpdate(BaseModel):
    nombre: Optional[str] = None
    afecto_igv: Optional[bool] = None
    activo: Optional[bool] = None


class ConceptoCargoResponse(ConceptoCargoBase):
    id: str


class FolioMovimientoBase(BaseModel):
    folio_id: str
    tipo: str
    concepto_id: Optional[str] = None
    descripcion: Optional[str] = None
    cantidad: float = 1
    precio_unitario: float = 0.00
    monto_total: float = 0.00
    metodo_pago: Optional[str] = None
    producto_id: Optional[str] = None
    usuario_id: Optional[str] = None


class FolioMovimientoCreate(FolioMovimientoBase):
    pass


class FolioMovimientoResponse(BaseModel):
    id: str
    folio_id: str
    tipo: str
    concepto_id: Optional[str] = None
    descripcion: Optional[str] = None
    cantidad: float
    precio_unitario: float
    monto_base: float
    monto_igv: float
    monto_servicio: float
    monto_total: float
    metodo_pago: Optional[str] = None
    producto_id: Optional[str] = None
    anulado: bool
    motivo_anulacion: Optional[str] = None
    usuario_id: Optional[str] = None
    creado_en: datetime


class FolioMovimientoAnular(BaseModel):
    motivo_anulacion: str


class ComprobanteCreate(BaseModel):
    folio_id: str
    tipo: str
    razon_social_cliente: Optional[str] = None
    ruc_dni_cliente: Optional[str] = None
    direccion_cliente: Optional[str] = None
    emitido_por: Optional[str] = None


class ComprobanteResponse(BaseModel):
    id: str
    hotel_id: str
    folio_id: str
    tipo: str
    serie: str
    correlativo: Optional[int] = None
    razon_social_cliente: Optional[str] = None
    ruc_dni_cliente: Optional[str] = None
    direccion_cliente: Optional[str] = None
    subtotal: float
    igv: float
    servicio: float
    total: float
    sunat_hash: Optional[str] = None
    estado: str
    emitido_en: datetime
