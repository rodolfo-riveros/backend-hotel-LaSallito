from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import (
    hoteles,
    auth,
    huespedes,
    reservas,
    estadias,
    folios,
    housekeeping,
    inventario,
    auditoria,
    dashboard,
)

app = FastAPI(
    title=settings.project_name,
    version="1.0.0",
    description="API REST del Sistema PMS Hotelero - IES La Salle",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prefix = settings.api_v1_prefix

app.include_router(hoteles.router, prefix=prefix)
app.include_router(auth.router, prefix=prefix)
app.include_router(huespedes.router, prefix=prefix)
app.include_router(reservas.router, prefix=prefix)
app.include_router(estadias.router, prefix=prefix)
app.include_router(folios.router, prefix=prefix)
app.include_router(housekeeping.router, prefix=prefix)
app.include_router(inventario.router, prefix=prefix)
app.include_router(auditoria.router, prefix=prefix)
app.include_router(dashboard.router, prefix=prefix)


@app.get("/")
async def root():
    return {
        "nombre": settings.project_name,
        "version": "1.0.0",
        "docs": f"{prefix}/docs",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
