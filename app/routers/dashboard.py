from fastapi import APIRouter, Depends
from supabase import Client
from typing import List
from app.core.database import get_supabase
from app.core.dependencies import get_current_user, get_hotel_id
from app.schemas.dashboard import (
    DashboardHoyResponse,
    HabitacionRackResponse,
    ReporteOcupacionResponse,
    ReporteIngresosResponse,
    HuespedInHouseResponse,
    HistorialHuespedResponse,
    PlanLimpiezaResponse,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard y Reportes"])


@router.get("/hoy", response_model=List[DashboardHoyResponse])
async def dashboard_hoy(
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("vw_dashboard_hoy").select("*").execute()
    return result.data


@router.get("/rack-habitaciones", response_model=List[HabitacionRackResponse])
async def rack_habitaciones(
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("vw_rack_habitaciones").select("*").execute()
    return result.data


@router.get("/reporte-ocupacion", response_model=List[ReporteOcupacionResponse])
async def reporte_ocupacion(
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("vw_reporte_ocupacion_diario").select("*").order("fecha", desc=True).execute()
    return result.data


@router.get("/reporte-ingresos", response_model=List[ReporteIngresosResponse])
async def reporte_ingresos(
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("vw_reporte_ingresos").select("*").order("fecha", desc=True).execute()
    return result.data


@router.get("/huespedes-in-house", response_model=List[HuespedInHouseResponse])
async def huespedes_in_house(
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("vw_huespedes_in_house").select("*").execute()
    return result.data


@router.get("/historial-huesped/{huesped_id}", response_model=List[HistorialHuespedResponse])
async def historial_huesped(
    huesped_id: str,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("vw_historial_huesped").select("*").eq("huesped_id", huesped_id).order("fecha_checkin_real", desc=True).execute()
    return result.data


@router.get("/plan-limpieza-hoy", response_model=List[PlanLimpiezaResponse])
async def plan_limpieza_hoy(
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("vw_plan_limpieza_hoy").select("*").execute()
    return result.data
