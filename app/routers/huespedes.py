from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from typing import List, Optional
from app.core.database import get_supabase
from app.core.dependencies import get_current_user, get_hotel_id, require_roles
from app.schemas.huesped import HuespedCreate, HuespedUpdate, HuespedResponse

router = APIRouter(prefix="/huespedes", tags=["Cardex - Huéspedes"])


@router.get("/", response_model=List[HuespedResponse])
async def listar_huespedes(
    hotel_id: str = Depends(get_hotel_id),
    search: Optional[str] = None,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    query = supabase.table("huespedes").select("*").eq("hotel_id", hotel_id)
    if search:
        query = query.or_(
            f"nombres.ilike.%{search}%,apellidos.ilike.%{search}%,"
            f"numero_documento.ilike.%{search}%,email.ilike.%{search}%"
        )
    result = query.order("apellidos", desc=False).execute()
    return result.data




@router.get("/{huesped_id}", response_model=HuespedResponse)
async def obtener_huesped(
    huesped_id: str,
    hotel_id: str = Depends(get_hotel_id),
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("huespedes").select("*").eq("id", huesped_id).eq("hotel_id", hotel_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Huésped no encontrado")
    return result.data[0]


@router.post("/", response_model=HuespedResponse, status_code=201)
async def crear_huesped(
    data: HuespedCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("recepcionista", "supervisor", "administrador")),
):
    result = supabase.table("huespedes").insert(data.model_dump(mode='json')).execute()
    return result.data[0]


@router.put("/{huesped_id}", response_model=HuespedResponse)
async def actualizar_huesped(
    huesped_id: str,
    data: HuespedUpdate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("recepcionista", "supervisor", "administrador")),
):
    update_data = {k: v for k, v in data.model_dump(mode='json').items() if v is not None}
    result = supabase.table("huespedes").update(update_data).eq("id", huesped_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Huésped no encontrado")
    return result.data[0]


@router.get("/buscar/documento", response_model=List[HuespedResponse])
async def buscar_huesped_por_documento(
    tipo_documento: str,
    numero_documento: str,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("huespedes").select("*").eq("tipo_documento", tipo_documento).eq("numero_documento", numero_documento).execute()
    return result.data
