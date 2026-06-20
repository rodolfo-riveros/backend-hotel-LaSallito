from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from typing import List
from app.core.database import get_supabase
from app.core.dependencies import get_current_user, get_hotel_id, require_roles
from app.schemas.estadia import (
    EstadiaCreate, EstadiaResponse,
    CheckinDocumentoVerificadoCreate, CheckinDocumentoVerificadoResponse,
)

router = APIRouter(prefix="/estadias", tags=["Check-in / Estadías"])


@router.get("/", response_model=List[EstadiaResponse])
async def listar_estadias(
    hotel_id: str = Depends(get_hotel_id),
    activas: bool = True,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    query = supabase.table("estadias").select("*").eq("hotel_id", hotel_id)
    if activas:
        query = query.is_("fecha_checkout_real", "null")
    result = query.order("fecha_checkin_real", desc=True).execute()
    return result.data


@router.get("/{estadia_id}", response_model=EstadiaResponse)
async def obtener_estadia(
    estadia_id: str,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("estadias").select("*").eq("id", estadia_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Estadía no encontrada")
    return result.data[0]


@router.post("/checkin", response_model=EstadiaResponse, status_code=201)
async def realizar_checkin(
    data: EstadiaCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("recepcionista", "administrador")),
):
    result = supabase.table("estadias").insert(data.model_dump()).execute()
    return result.data[0]


@router.post("/{estadia_id}/checkout")
async def realizar_checkout(
    estadia_id: str,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("recepcionista", "administrador")),
):
    folio = supabase.table("folios").select("*").eq("estadia_id", estadia_id).execute()
    if not folio.data:
        raise HTTPException(status_code=404, detail="Folio no encontrado")

    result = supabase.table("folios").update({"abierto": False}).eq("id", folio.data[0]["id"]).execute()
    return {"mensaje": "Check-out realizado correctamente", "folio": result.data[0]}


@router.put("/{estadia_id}/calificar", response_model=EstadiaResponse)
async def calificar_estadia(
    estadia_id: str,
    calificacion: int,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    if calificacion < 1 or calificacion > 5:
        raise HTTPException(status_code=400, detail="Calificación debe ser entre 1 y 5")
    result = supabase.table("estadias").update({"calificacion": calificacion}).eq("id", estadia_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Estadía no encontrada")
    return result.data[0]


@router.post("/documentos-verificados", response_model=CheckinDocumentoVerificadoResponse, status_code=201)
async def verificar_documento(
    data: CheckinDocumentoVerificadoCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("checkin_documentos_verificados").insert(data.model_dump()).execute()
    return result.data[0]
