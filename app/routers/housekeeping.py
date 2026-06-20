from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from typing import List, Optional
from datetime import date
from app.core.database import get_supabase
from app.core.dependencies import get_current_user, get_hotel_id, require_roles
from app.schemas.housekeeping import (
    TareaLimpiezaCreate, TareaLimpiezaUpdate, TareaLimpiezaResponse,
    ObjetoPerdidoCreate, ObjetoPerdidoUpdate, ObjetoPerdidoResponse,
)

router = APIRouter(prefix="/housekeeping", tags=["Housekeeping"])


# === TAREAS DE LIMPIEZA ===

@router.get("/tareas-limpieza", response_model=List[TareaLimpiezaResponse])
async def listar_tareas_limpieza(
    hotel_id: str = Depends(get_hotel_id),
    fecha: Optional[date] = None,
    estado: Optional[str] = None,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    query = supabase.table("tareas_limpieza").select("*").eq("hotel_id", hotel_id)
    if fecha:
        query = query.eq("fecha", fecha.isoformat())
    if estado:
        query = query.eq("estado", estado)
    result = query.order("fecha", desc=False).execute()
    return result.data


@router.post("/tareas-limpieza", response_model=TareaLimpiezaResponse, status_code=201)
async def crear_tarea_limpieza(
    data: TareaLimpiezaCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("ama_llaves", "supervisor", "administrador")),
):
    result = supabase.table("tareas_limpieza").insert(data.model_dump()).execute()
    return result.data[0]


@router.put("/tareas-limpieza/{tarea_id}", response_model=TareaLimpiezaResponse)
async def actualizar_tarea_limpieza(
    tarea_id: str,
    data: TareaLimpiezaUpdate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("ama_llaves", "supervisor", "administrador")),
):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    result = supabase.table("tareas_limpieza").update(update_data).eq("id", tarea_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return result.data[0]


@router.post("/tareas-limpieza/{tarea_id}/asignar", response_model=TareaLimpiezaResponse)
async def asignar_tarea_limpieza(
    tarea_id: str,
    usuario_id: str,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("ama_llaves", "supervisor", "administrador")),
):
    result = supabase.table("tareas_limpieza").update({
        "asignado_a": usuario_id,
        "estado": "en_proceso",
    }).eq("id", tarea_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return result.data[0]


# === OBJETOS PERDIDOS ===

@router.get("/objetos-perdidos", response_model=List[ObjetoPerdidoResponse])
async def listar_objetos_perdidos(
    hotel_id: str = Depends(get_hotel_id),
    entregado: Optional[bool] = None,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    query = supabase.table("objetos_perdidos").select("*").eq("hotel_id", hotel_id)
    if entregado is not None:
        query = query.eq("entregado", entregado)
    result = query.order("encontrado_en", desc=True).execute()
    return result.data


@router.post("/objetos-perdidos", response_model=ObjetoPerdidoResponse, status_code=201)
async def registrar_objeto_perdido(
    data: ObjetoPerdidoCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("ama_llaves", "supervisor", "administrador")),
):
    result = supabase.table("objetos_perdidos").insert(data.model_dump()).execute()
    return result.data[0]


@router.put("/objetos-perdidos/{objeto_id}", response_model=ObjetoPerdidoResponse)
async def actualizar_objeto_perdido(
    objeto_id: str,
    data: ObjetoPerdidoUpdate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("ama_llaves", "supervisor", "administrador")),
):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if data.entregado:
        update_data["entregado_en"] = "now()"
    result = supabase.table("objetos_perdidos").update(update_data).eq("id", objeto_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Objeto no encontrado")
    return result.data[0]
