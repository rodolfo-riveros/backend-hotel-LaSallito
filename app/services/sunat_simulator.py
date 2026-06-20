import hashlib
from datetime import datetime, timezone
from supabase import Client

SERIES = {"boleta": "B001", "factura": "F001"}


def emitir_comprobante(
    supabase: Client,
    hotel_id: str,
    folio_id: str,
    tipo: str,
    razon_social_cliente: str | None = None,
    ruc_dni_cliente: str | None = None,
    direccion_cliente: str | None = None,
    emitido_por: str | None = None,
) -> dict:
    movs = supabase.table("folio_movimientos") \
        .select("tipo, monto_total, anulado") \
        .eq("folio_id", folio_id) \
        .execute()

    cargos = sum(
        m["monto_total"] for m in movs.data
        if m["tipo"] == "cargo" and not m["anulado"]
    )
    pagos = sum(
        m["monto_total"] for m in movs.data
        if m["tipo"] == "pago" and not m["anulado"]
    )
    total = cargos - pagos

    if total <= 0:
        raise ValueError("No hay cargos pendientes por facturar. Saldo: 0 o negativo.")

    hotel = supabase.table("hoteles").select("porcentaje_servicio").eq("id", hotel_id).execute()
    servicio_pct = (hotel.data[0]["porcentaje_servicio"] / 100) if hotel.data else 0.00
    igv_pct = 0.18

    base = total / (1 + igv_pct + servicio_pct)
    monto_igv = base * igv_pct
    monto_servicio = base * servicio_pct

    serie = SERIES.get(tipo, "B001")
    ultimo = supabase.table("comprobantes") \
        .select("correlativo") \
        .eq("hotel_id", hotel_id) \
        .eq("serie", serie) \
        .order("correlativo", desc=True) \
        .limit(1) \
        .execute()
    correlativo = (ultimo.data[0]["correlativo"] + 1) if ultimo.data else 1

    raw = (
        f"{serie}|{correlativo}|{total:.2f}|{folio_id}|"
        f"{datetime.now(timezone.utc).isoformat()}|{hotel_id}"
    )
    sunat_hash = hashlib.sha256(raw.encode()).hexdigest().upper()

    data = {
        "hotel_id": hotel_id,
        "folio_id": folio_id,
        "tipo": tipo,
        "serie": serie,
        "correlativo": correlativo,
        "razon_social_cliente": razon_social_cliente,
        "ruc_dni_cliente": ruc_dni_cliente,
        "direccion_cliente": direccion_cliente,
        "subtotal": round(base, 2),
        "igv": round(monto_igv, 2),
        "servicio": round(monto_servicio, 2),
        "total": round(total, 2),
        "sunat_hash": sunat_hash,
        "estado": "emitido",
        "emitido_por": emitido_por,
    }

    result = supabase.table("comprobantes").insert(data).execute()
    return result.data[0]
