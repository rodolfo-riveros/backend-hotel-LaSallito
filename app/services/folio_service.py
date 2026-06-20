from supabase import Client


def calcular_totales_folio(supabase: Client, folio_id: str) -> dict:
    movimientos = supabase.table("folio_movimientos").select(
        "tipo, monto_total, anulado"
    ).eq("folio_id", folio_id).execute()

    cargos = sum(
        m["monto_total"] for m in movimientos.data
        if m["tipo"] == "cargo" and not m["anulado"]
    )
    pagos = sum(
        m["monto_total"] for m in movimientos.data
        if m["tipo"] == "pago" and not m["anulado"]
    )
    saldo = cargos - pagos

    supabase.table("folios").update({"saldo": saldo}).eq("id", folio_id).execute()
    return {"cargos": cargos, "pagos": pagos, "saldo": saldo}


def get_movimientos_por_folio(supabase: Client, folio_id: str) -> list:
    result = supabase.table("folio_movimientos").select(
        "*, conceptos_cargo!inner(nombre)"
    ).eq("folio_id", folio_id).order("creado_en").execute()
    return result.data
