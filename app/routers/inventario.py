from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from typing import List, Optional
from app.core.database import get_supabase
from app.core.dependencies import get_current_user, get_hotel_id, require_roles
from app.schemas.inventario import (
    ProductoCreate, ProductoUpdate, ProductoResponse,
    InventarioMovimientoCreate, InventarioMovimientoResponse,
)

router = APIRouter(prefix="/inventario", tags=["Inventario"])


# === PRODUCTOS ===

@router.get("/productos", response_model=List[ProductoResponse])
async def listar_productos(
    hotel_id: str = Depends(get_hotel_id),
    stock_bajo: bool = False,
    categoria: Optional[str] = None,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    query = supabase.table("productos").select("*").eq("hotel_id", hotel_id)
    if categoria:
        query = query.eq("categoria", categoria)
    result = query.execute()
    if stock_bajo:
        result.data = [p for p in result.data if p["stock_actual"] <= p["stock_minimo"]]
    return result.data


@router.get("/productos/{producto_id}", response_model=ProductoResponse)
async def obtener_producto(
    producto_id: str,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("productos").select("*").eq("id", producto_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return result.data[0]


@router.post("/productos", response_model=ProductoResponse, status_code=201)
async def crear_producto(
    data: ProductoCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("supervisor", "administrador")),
):
    result = supabase.table("productos").insert(data.model_dump()).execute()
    return result.data[0]


@router.put("/productos/{producto_id}", response_model=ProductoResponse)
async def actualizar_producto(
    producto_id: str,
    data: ProductoUpdate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("supervisor", "administrador")),
):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    result = supabase.table("productos").update(update_data).eq("id", producto_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return result.data[0]


# === MOVIMIENTOS DE INVENTARIO ===

@router.get("/movimientos", response_model=List[InventarioMovimientoResponse])
async def listar_movimientos_inventario(
    hotel_id: str = Depends(get_hotel_id),
    producto_id: Optional[str] = None,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    query = supabase.table("inventario_movimientos").select("*").eq("hotel_id", hotel_id)
    if producto_id:
        query = query.eq("producto_id", producto_id)
    result = query.order("creado_en", desc=True).execute()
    return result.data


@router.post("/movimientos", response_model=InventarioMovimientoResponse, status_code=201)
async def crear_movimiento_inventario(
    data: InventarioMovimientoCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("supervisor", "administrador")),
):
    result = supabase.table("inventario_movimientos").insert(data.model_dump()).execute()
    return result.data[0]
