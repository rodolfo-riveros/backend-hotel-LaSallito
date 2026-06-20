from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
from app.core.database import get_supabase
from app.core.security import get_current_user
from app.schemas.perfil import (
    LoginRequest, RegisterRequest, AuthResponse,
    PerfilCreate, PerfilUpdate, PerfilResponse,
)
from typing import List

router = APIRouter(prefix="/auth", tags=["Auth & Perfiles"])


@router.post("/login", response_model=AuthResponse)
async def login(
    data: LoginRequest,
    supabase: Client = Depends(get_supabase),
):
    try:
        auth_result = supabase.auth.sign_in_with_password(
            {"email": data.email, "password": data.password}
        )
        user_id = auth_result.user.id
        perfil = supabase.table("perfiles").select("*").eq("id", user_id).execute()
        if not perfil.data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Perfil no encontrado",
            )
        return AuthResponse(
            access_token=auth_result.session.access_token,
            user=PerfilResponse(**perfil.data[0]),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/register", response_model=PerfilResponse, status_code=201)
async def register(
    data: RegisterRequest,
    supabase: Client = Depends(get_supabase),
):
    try:
        auth_result = supabase.auth.admin.create_user({
            "email": data.email,
            "password": data.password,
            "email_confirm": True,
        })
        user_id = auth_result.user.id
        insert_data = {
            "id": user_id,
            "nombre_completo": data.nombre_completo,
            "rol": data.rol,
            "hotel_id": data.hotel_id,
            "codigo_estudiante": data.codigo_estudiante,
            "activo": True,
        }
        result = supabase.table("perfiles").insert(insert_data).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/perfiles", response_model=List[PerfilResponse])
async def listar_perfiles(
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("perfiles").select("*").execute()
    return result.data


@router.get("/perfiles/{perfil_id}", response_model=PerfilResponse)
async def obtener_perfil(
    perfil_id: str,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("perfiles").select("*").eq("id", perfil_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return result.data[0]


@router.put("/perfiles/{perfil_id}", response_model=PerfilResponse)
async def actualizar_perfil(
    perfil_id: str,
    data: PerfilUpdate,
    supabase: Client = Depends(get_supabase),
    current_user: dict = Depends(get_current_user),
):
    if current_user["id"] != perfil_id and current_user["rol"] != "administrador":
        raise HTTPException(status_code=403, detail="No autorizado")
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    result = supabase.table("perfiles").update(update_data).eq("id", perfil_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return result.data[0]


@router.get("/me", response_model=PerfilResponse)
async def perfil_actual(
    current_user: dict = Depends(get_current_user),
):
    return PerfilResponse(**current_user)
