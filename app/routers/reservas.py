from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from typing import List, Optional
from datetime import date, datetime
from app.core.database import get_supabase
from app.core.dependencies import get_current_user, get_hotel_id, require_roles
from app.schemas.reserva import (
    ReservaCreate, ReservaUpdate, ReservaResponse,
    ReservaHuespedAdicionalCreate, ReservaHuespedAdicionalResponse,
)

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.get("/", response_model=List[ReservaResponse])
async def listar_reservas(
    hotel_id: str = Depends(get_hotel_id),
    estado: Optional[str] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    query = supabase.table("reservas").select("*").eq("hotel_id", hotel_id)
    if estado:
        query = query.eq("estado", estado)
    if fecha_desde:
        query = query.gte("fecha_llegada", fecha_desde.isoformat())
    if fecha_hasta:
        query = query.lte("fecha_salida", fecha_hasta.isoformat())
    result = query.order("fecha_llegada", desc=False).execute()
    return result.data


@router.get("/{reserva_id}", response_model=ReservaResponse)
async def obtener_reserva(
    reserva_id: str,
    hotel_id: str = Depends(get_hotel_id),
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("reservas").select("*").eq("id", reserva_id).eq("hotel_id", hotel_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return result.data[0]


@router.post("/", response_model=ReservaResponse, status_code=201)
async def crear_reserva(
    data: ReservaCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("recepcionista", "supervisor", "administrador")),
):
    huespedes_adicionales = data.huespedes_adicionales or []
    base_data = data.model_dump(exclude={"huespedes_adicionales"}, mode='json')
    base_data["codigo_reserva"] = f"RES-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{data.huesped_id[:6]}"
    result = supabase.table("reservas").insert(base_data).execute()
    reserva = result.data[0]

    for h_id in huespedes_adicionales:
        supabase.table("reserva_huespedes_adicionales").insert({
            "reserva_id": reserva["id"],
            "huesped_id": h_id,
        }).execute()

    return reserva


@router.put("/{reserva_id}", response_model=ReservaResponse)
async def actualizar_reserva(
    reserva_id: str,
    data: ReservaUpdate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("recepcionista", "supervisor", "administrador")),
):
    update_data = {k: v for k, v in data.model_dump(mode='json').items() if v is not None}
    result = supabase.table("reservas").update(update_data).eq("id", reserva_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return result.data[0]


@router.post("/{reserva_id}/cancelar", response_model=ReservaResponse)
async def cancelar_reserva(
    reserva_id: str,
    motivo: str,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("recepcionista", "supervisor", "administrador")),
):
    result = supabase.table("reservas").update({
        "estado": "cancelada",
        "motivo_cancelacion": motivo,
    }).eq("id", reserva_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return result.data[0]


@router.post("/{reserva_id}/huespedes-adicionales", response_model=ReservaHuespedAdicionalResponse, status_code=201)
async def agregar_huesped_adicional(
    reserva_id: str,
    data: ReservaHuespedAdicionalCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("reserva_huespedes_adicionales").insert(data.model_dump(mode='json')).execute()
    return result.data[0]
