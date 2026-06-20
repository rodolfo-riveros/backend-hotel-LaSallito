from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PerfilBase(BaseModel):
    hotel_id: Optional[str] = None
    nombre_completo: str
    rol: str
    codigo_estudiante: Optional[str] = None
    activo: bool = True


class PerfilCreate(PerfilBase):
    id: str
    email: Optional[str] = None


class PerfilUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    rol: Optional[str] = None
    codigo_estudiante: Optional[str] = None
    activo: Optional[bool] = None


class PerfilResponse(PerfilBase):
    id: str
    creado_en: datetime


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    nombre_completo: str
    rol: str = "recepcionista"
    hotel_id: Optional[str] = None
    codigo_estudiante: Optional[str] = None


class AuthResponse(BaseModel):
    access_token: str
    user: PerfilResponse
