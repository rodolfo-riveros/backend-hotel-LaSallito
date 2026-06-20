from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from typing import List, Optional
from datetime import date
from app.core.database import get_supabase
from app.core.dependencies import get_hotel_id, require_roles
from app.schemas.auditoria import (
    AuditoriaResponse,
    CierreNocturnoCreate, CierreNocturnoResponse,
)

router = APIRouter(prefix="/auditoria", tags=["Auditoría y Cierre Nocturno"])


# === AUDITORÍA ===

@router.get("/", response_model=List[AuditoriaResponse])
async def listar_auditoria(
    hotel_id: str = Depends(get_hotel_id),
    tabla_afectada: Optional[str] = None,
    accion: Optional[str] = None,
    limit: int = 100,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("administrador", "auditor_nocturno")),
):
    query = supabase.table("auditoria").select("*").eq("hotel_id", hotel_id)
    if tabla_afectada:
        query = query.eq("tabla_afectada", tabla_afectada)
    if accion:
        query = query.eq("accion", accion)
    result = query.order("creado_en", desc=True).limit(limit).execute()
    return result.data


# === CIERRES NOCTURNOS ===

@router.get("/cierres-nocturnos", response_model=List[CierreNocturnoResponse])
async def listar_cierres(
    hotel_id: str = Depends(get_hotel_id),
    fecha_desde: Optional[date] = None,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("administrador", "auditor_nocturno")),
):
    query = supabase.table("cierres_nocturnos").select("*").eq("hotel_id", hotel_id)
    if fecha_desde:
        query = query.gte("fecha", fecha_desde.isoformat())
    result = query.order("fecha", desc=True).execute()
    return result.data


@router.post("/cierres-nocturnos", response_model=CierreNocturnoResponse, status_code=201)
async def crear_cierre_nocturno(
    data: CierreNocturnoCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("auditor_nocturno", "administrador")),
):
    result = supabase.table("cierres_nocturnos").insert(data.model_dump()).execute()
    return result.data[0]
