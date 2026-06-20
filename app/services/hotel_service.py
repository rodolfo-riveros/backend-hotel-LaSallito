from supabase import Client
from app.schemas.hotel import HotelResponse


def get_hotel_config(supabase: Client, hotel_id: str) -> dict:
    result = supabase.table("hoteles").select("*").eq("id", hotel_id).execute()
    if not result.data:
        return {}
    return result.data[0]


def get_disponibilidad_habitaciones(
    supabase: Client, hotel_id: str, tipo_habitacion_id: str | None = None
) -> list:
    query = supabase.table("habitaciones").select(
        "id, numero, piso, tipo_habitacion_id, estado"
    ).eq("hotel_id", hotel_id).eq("activo", True).eq("estado", "libre")
    if tipo_habitacion_id:
        query = query.eq("tipo_habitacion_id", tipo_habitacion_id)
    result = query.execute()
    return result.data
