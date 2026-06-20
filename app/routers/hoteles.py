from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from typing import List
from app.core.database import get_supabase
from app.core.security import get_admin_user
from app.core.dependencies import get_hotel_id
from app.schemas.hotel import (
    HotelCreate, HotelUpdate, HotelResponse,
    TipoHabitacionCreate, TipoHabitacionUpdate, TipoHabitacionResponse,
    HabitacionCreate, HabitacionUpdate, HabitacionResponse,
    TemporadaCreate, TemporadaUpdate, TemporadaResponse,
    TarifaCreate, TarifaUpdate, TarifaResponse,
    PoliticaCancelacionCreate, PoliticaCancelacionUpdate, PoliticaCancelacionResponse,
)

router = APIRouter(prefix="/hoteles", tags=["Configuración - Hotel"])


@router.get("/", response_model=List[HotelResponse])
async def listar_hoteles(
    supabase: Client = Depends(get_supabase),
    _=Depends(get_admin_user),
):
    result = supabase.table("hoteles").select("*").execute()
    return result.data


@router.get("/{hotel_id}", response_model=HotelResponse)
async def obtener_hotel(
    hotel_id: str,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_admin_user),
):
    result = supabase.table("hoteles").select("*").eq("id", hotel_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    return result.data[0]


@router.post("/", response_model=HotelResponse, status_code=201)
async def crear_hotel(
    data: HotelCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_admin_user),
):
    result = supabase.table("hoteles").insert(data.model_dump()).execute()
    return result.data[0]


@router.put("/{hotel_id}", response_model=HotelResponse)
async def actualizar_hotel(
    hotel_id: str,
    data: HotelUpdate,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_admin_user),
):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    result = supabase.table("hoteles").update(update_data).eq("id", hotel_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    return result.data[0]


# === TIPOS DE HABITACIÓN ===

@router.get("/{hotel_id}/tipos-habitacion", response_model=List[TipoHabitacionResponse])
async def listar_tipos_habitacion(
    hotel_id: str,
    supabase: Client = Depends(get_supabase),
):
    result = supabase.table("tipos_habitacion").select("*").eq("hotel_id", hotel_id).execute()
    return result.data


@router.post("/{hotel_id}/tipos-habitacion", response_model=TipoHabitacionResponse, status_code=201)
async def crear_tipo_habitacion(
    hotel_id: str,
    data: TipoHabitacionCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_admin_user),
):
    data.hotel_id = hotel_id
    result = supabase.table("tipos_habitacion").insert(data.model_dump()).execute()
    return result.data[0]


@router.put("/{hotel_id}/tipos-habitacion/{tipo_id}", response_model=TipoHabitacionResponse)
async def actualizar_tipo_habitacion(
    hotel_id: str,
    tipo_id: str,
    data: TipoHabitacionUpdate,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_admin_user),
):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    result = supabase.table("tipos_habitacion").update(update_data).eq("id", tipo_id).eq("hotel_id", hotel_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Tipo de habitación no encontrado")
    return result.data[0]


# === HABITACIONES ===

@router.get("/{hotel_id}/habitaciones", response_model=List[HabitacionResponse])
async def listar_habitaciones(
    hotel_id: str,
    estado: str | None = None,
    supabase: Client = Depends(get_supabase),
):
    query = supabase.table("habitaciones").select("*").eq("hotel_id", hotel_id)
    if estado:
        query = query.eq("estado", estado)
    result = query.execute()
    return result.data


@router.post("/{hotel_id}/habitaciones", response_model=HabitacionResponse, status_code=201)
async def crear_habitacion(
    hotel_id: str,
    data: HabitacionCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_admin_user),
):
    data.hotel_id = hotel_id
    result = supabase.table("habitaciones").insert(data.model_dump()).execute()
    return result.data[0]


@router.put("/{hotel_id}/habitaciones/{habitacion_id}", response_model=HabitacionResponse)
async def actualizar_habitacion(
    hotel_id: str,
    habitacion_id: str,
    data: HabitacionUpdate,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_admin_user),
):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    result = supabase.table("habitaciones").update(update_data).eq("id", habitacion_id).eq("hotel_id", hotel_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    return result.data[0]


# === TEMPORADAS ===

@router.get("/{hotel_id}/temporadas", response_model=List[TemporadaResponse])
async def listar_temporadas(
    hotel_id: str,
    supabase: Client = Depends(get_supabase),
):
    result = supabase.table("temporadas").select("*").eq("hotel_id", hotel_id).execute()
    return result.data


@router.post("/{hotel_id}/temporadas", response_model=TemporadaResponse, status_code=201)
async def crear_temporada(
    hotel_id: str,
    data: TemporadaCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_admin_user),
):
    data.hotel_id = hotel_id
    result = supabase.table("temporadas").insert(data.model_dump()).execute()
    return result.data[0]


# === TARIFAS ===

@router.get("/{hotel_id}/tarifas", response_model=List[TarifaResponse])
async def listar_tarifas(
    hotel_id: str,
    tipo_habitacion_id: str | None = None,
    supabase: Client = Depends(get_supabase),
):
    query = supabase.table("tarifas").select("*").eq("hotel_id", hotel_id)
    if tipo_habitacion_id:
        query = query.eq("tipo_habitacion_id", tipo_habitacion_id)
    result = query.execute()
    return result.data


@router.post("/{hotel_id}/tarifas", response_model=TarifaResponse, status_code=201)
async def crear_tarifa(
    hotel_id: str,
    data: TarifaCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_admin_user),
):
    data.hotel_id = hotel_id
    result = supabase.table("tarifas").insert(data.model_dump()).execute()
    return result.data[0]


@router.put("/{hotel_id}/tarifas/{tarifa_id}", response_model=TarifaResponse)
async def actualizar_tarifa(
    hotel_id: str,
    tarifa_id: str,
    data: TarifaUpdate,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_admin_user),
):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    result = supabase.table("tarifas").update(update_data).eq("id", tarifa_id).eq("hotel_id", hotel_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Tarifa no encontrada")
    return result.data[0]


# === POLÍTICAS DE CANCELACIÓN ===

@router.get("/{hotel_id}/politicas-cancelacion", response_model=List[PoliticaCancelacionResponse])
async def listar_politicas_cancelacion(
    hotel_id: str,
    supabase: Client = Depends(get_supabase),
):
    result = supabase.table("politicas_cancelacion").select("*").eq("hotel_id", hotel_id).execute()
    return result.data


@router.post("/{hotel_id}/politicas-cancelacion", response_model=PoliticaCancelacionResponse, status_code=201)
async def crear_politica_cancelacion(
    hotel_id: str,
    data: PoliticaCancelacionCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_admin_user),
):
    data.hotel_id = hotel_id
    result = supabase.table("politicas_cancelacion").insert(data.model_dump()).execute()
    return result.data[0]
