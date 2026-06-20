from supabase import Client
from datetime import date


def buscar_habitaciones_disponibles(
    supabase: Client,
    hotel_id: str,
    tipo_habitacion_id: str,
    fecha_llegada: date,
    fecha_salida: date,
) -> list:
    habitaciones_ocupadas = supabase.table("estadias").select(
        "habitacion_id"
    ).eq("hotel_id", hotel_id).is_("fecha_checkout_real", "null").execute()

    ids_ocupadas = [h["habitacion_id"] for h in habitaciones_ocupadas.data]

    query = supabase.table("habitaciones").select("*").eq(
        "hotel_id", hotel_id
    ).eq("tipo_habitacion_id", tipo_habitacion_id).eq("activo", True).eq("estado", "libre")

    result = query.execute()
    disponibles = [h for h in result.data if h["id"] not in ids_ocupadas]
    return disponibles


async def calcular_precio_estadia(
    supabase: Client,
    tipo_habitacion_id: str,
    fecha_llegada: date,
    fecha_salida: date,
) -> dict:
    noches = (fecha_salida - fecha_llegada).days
    tarifas = supabase.table("tarifas").select(
        "*, temporadas!left(fecha_inicio, fecha_fin)"
    ).eq("tipo_habitacion_id", tipo_habitacion_id).eq("activo", True).execute()

    mejor_precio = 0
    for t in tarifas.data:
        if t.get("temporada_id"):
            temp = supabase.table("temporadas").select("*").eq("id", t["temporada_id"]).execute()
            if temp.data:
                if temp.data[0]["fecha_inicio"] <= fecha_llegada <= temp.data[0]["fecha_fin"]:
                    mejor_precio = t["precio_noche"]
                    break
        else:
            if not mejor_precio or t["precio_noche"] < mejor_precio:
                mejor_precio = t["precio_noche"]

    return {"precio_noche": mejor_precio, "noches": noches, "total": mejor_precio * noches}
