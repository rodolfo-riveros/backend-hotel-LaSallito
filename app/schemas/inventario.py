from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductoBase(BaseModel):
    hotel_id: str
    codigo: str
    nombre: str
    categoria: Optional[str] = None
    unidad_medida: str = "unidad"
    precio_compra: float = 0.00
    precio_venta: float = 0.00
    stock_actual: float = 0.00
    stock_minimo: float = 0.00
    activo: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    unidad_medida: Optional[str] = None
    precio_compra: Optional[float] = None
    precio_venta: Optional[float] = None
    stock_actual: Optional[float] = None
    stock_minimo: Optional[float] = None
    activo: Optional[bool] = None


class ProductoResponse(ProductoBase):
    id: str
    creado_en: datetime


class InventarioMovimientoCreate(BaseModel):
    hotel_id: str
    producto_id: str
    tipo: str
    cantidad: float = Field(gt=0)
    motivo: Optional[str] = None
    folio_movimiento_id: Optional[str] = None
    usuario_id: Optional[str] = None


class InventarioMovimientoResponse(BaseModel):
    id: str
    hotel_id: str
    producto_id: str
    tipo: str
    cantidad: float
    motivo: Optional[str] = None
    folio_movimiento_id: Optional[str] = None
    usuario_id: Optional[str] = None
    creado_en: datetime
