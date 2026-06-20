from fastapi import Depends, HTTPException, status
from app.core.database import get_supabase
from app.core.security import get_current_user
from supabase import Client
from typing import Optional


def get_hotel_id(
    current_user: dict = Depends(get_current_user),
) -> Optional[str]:
    hotel_id = current_user.get("hotel_id")
    if not hotel_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario sin hotel asignado",
        )
    return hotel_id


def require_roles(*roles: str):
    async def role_checker(
        current_user: dict = Depends(get_current_user),
    ):
        if current_user["rol"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de los roles: {', '.join(roles)}",
            )
        return current_user

    return role_checker


def get_supabase_client() -> Client:
    return get_supabase()
