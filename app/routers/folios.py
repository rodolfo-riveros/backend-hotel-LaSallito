from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from typing import List
from app.core.database import get_supabase
from app.core.dependencies import get_current_user, get_hotel_id, require_roles
from app.services.sunat_simulator import emitir_comprobante as emitir_sunat
from app.schemas.folio import (
    FolioResponse,
    ConceptoCargoCreate, ConceptoCargoUpdate, ConceptoCargoResponse,
    FolioMovimientoCreate, FolioMovimientoResponse, FolioMovimientoAnular,
    ComprobanteCreate, ComprobanteResponse,
)

router = APIRouter(prefix="/folios", tags=["Folio y Facturación"])


# === FOLIOS ===

@router.get("/", response_model=List[FolioResponse])
async def listar_folios(
    hotel_id: str = Depends(get_hotel_id),
    abiertos: bool = True,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    query = supabase.table("folios").select("*").eq("hotel_id", hotel_id)
    if abiertos:
        query = query.eq("abierto", True)
    result = query.execute()
    return result.data


@router.get("/{folio_id}", response_model=FolioResponse)
async def obtener_folio(
    folio_id: str,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("folios").select("*").eq("id", folio_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Folio no encontrado")
    return result.data[0]


# === CONCEPTOS DE CARGO ===

@router.get("/conceptos-cargo", response_model=List[ConceptoCargoResponse])
async def listar_conceptos_cargo(
    hotel_id: str = Depends(get_hotel_id),
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("conceptos_cargo").select("*").eq("hotel_id", hotel_id).execute()
    return result.data


@router.post("/conceptos-cargo", response_model=ConceptoCargoResponse, status_code=201)
async def crear_concepto_cargo(
    data: ConceptoCargoCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("administrador", "supervisor")),
):
    result = supabase.table("conceptos_cargo").insert(data.model_dump()).execute()
    return result.data[0]


@router.put("/conceptos-cargo/{concepto_id}", response_model=ConceptoCargoResponse)
async def actualizar_concepto_cargo(
    concepto_id: str,
    data: ConceptoCargoUpdate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("administrador", "supervisor")),
):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    result = supabase.table("conceptos_cargo").update(update_data).eq("id", concepto_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Concepto no encontrado")
    return result.data[0]


# === MOVIMIENTOS DEL FOLIO ===

@router.get("/{folio_id}/movimientos", response_model=List[FolioMovimientoResponse])
async def listar_movimientos(
    folio_id: str,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("folio_movimientos").select("*").eq("folio_id", folio_id).order("creado_en", desc=False).execute()
    return result.data


@router.post("/{folio_id}/movimientos", response_model=FolioMovimientoResponse, status_code=201)
async def crear_movimiento(
    folio_id: str,
    data: FolioMovimientoCreate,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("recepcionista", "administrador")),
):
    data.folio_id = folio_id
    insert_data = data.model_dump()

    if data.concepto_id:
        concepto = supabase.table("conceptos_cargo").select("afecto_igv").eq("id", data.concepto_id).execute()
        afecto_igv = concepto.data[0]["afecto_igv"] if concepto.data else True
    else:
        afecto_igv = True

    igv_pct = 0.18
    service_pct = 0.00

    if afecto_igv:
        base = data.monto_total / (1 + igv_pct + service_pct)
        monto_igv = base * igv_pct
        monto_servicio = base * service_pct
    else:
        base = data.monto_total
        monto_igv = 0.00
        monto_servicio = 0.00

    insert_data["monto_base"] = round(base, 2)
    insert_data["monto_igv"] = round(monto_igv, 2)
    insert_data["monto_servicio"] = round(monto_servicio, 2)

    result = supabase.table("folio_movimientos").insert(insert_data).execute()
    return result.data[0]


@router.put("/movimientos/{movimiento_id}/anular", response_model=FolioMovimientoResponse)
async def anular_movimiento(
    movimiento_id: str,
    data: FolioMovimientoAnular,
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("administrador", "supervisor")),
):
    result = supabase.table("folio_movimientos").update({
        "anulado": True,
        "motivo_anulacion": data.motivo_anulacion,
    }).eq("id", movimiento_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return result.data[0]


# === COMPROBANTES ===

@router.post("/{folio_id}/comprobantes", response_model=ComprobanteResponse, status_code=201)
async def emitir_comprobante(
    folio_id: str,
    data: ComprobanteCreate,
    hotel_id: str = Depends(get_hotel_id),
    supabase: Client = Depends(get_supabase),
    _=Depends(require_roles("recepcionista", "administrador")),
):
    try:
        result = emitir_sunat(
            supabase=supabase,
            hotel_id=hotel_id,
            folio_id=folio_id,
            tipo=data.tipo,
            razon_social_cliente=data.razon_social_cliente,
            ruc_dni_cliente=data.ruc_dni_cliente,
            direccion_cliente=data.direccion_cliente,
            emitido_por=data.emitido_por,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/comprobantes/{comprobante_id}", response_model=ComprobanteResponse)
async def obtener_comprobante(
    comprobante_id: str,
    supabase: Client = Depends(get_supabase),
    _=Depends(get_current_user),
):
    result = supabase.table("comprobantes").select("*").eq("id", comprobante_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Comprobante no encontrado")
    return result.data[0]
