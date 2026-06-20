# AGENTS.md — Hotel IES La Salle PMS Backend

## Stack

- **Runtime:** Python 3.14 (CPython)
- **Framework:** FastAPI (uvicorn)
- **Database:** Supabase (no local DB; all queries via `supabase` Python SDK)
- **Auth:** Supabase Auth JWT (`HTTPBearer`). Roles: `administrador`, `recepcionista`, `supervisor`
- **Config:** `pydantic-settings` reads `.env` (not checked in; template in `.env.example`)
- **Package mgr:** `uv` (venv was created with uv 0.11.8)

## Project layout

```
app/
  main.py           — FastAPI app creation, CORS, router registration
  core/
    config.py       — Settings class (reads .env)
    database.py     — Lazy singleton Supabase client
    security.py     — JWT extraction via Supabase Auth
    dependencies.py — get_hotel_id, require_roles helpers
  routers/          — One file per domain (auth, hoteles, reservas, etc.)
  schemas/          — Pydantic v2 models per domain
  services/         — Business logic (available rooms, price calc, etc.)
```

All routers are registered in `main.py` under `settings.api_v1_prefix` (default `/api/v1`).

## Commands

```bash
# Install dependencies
uv pip install -r requirements.txt

# Run dev server (hot-reload)
uvicorn app.main:app --reload --port 8000

# Run on a specific host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Notable quirks

- **No tests, no linter, no formatter, no CI** — none exist in the repo. Do not create them unless explicitly asked.
- **Supabase dependency** is imported directly in routers; no ORM abstraction layer.
- **Services layer** is thin — only 4 services exist (`hotel_service.py`, `folio_service.py`, `reserva_service.py`, `sunat_simulator.py`). Business logic lives inline in router endpoints.
- **Pydantic v2** is used (BaseModel, not v1).
- **File naming**: Spanish throughout (hoteles, huespedes, reservas, estadias, folios, etc.). Route paths match.
- **Auth flow**: `POST /auth/login` → returns `access_token` (JWT). All protected endpoints use `Authorization: Bearer <token>`. Token is verified against Supabase Auth via `supabase.auth.get_user(token)`, then the user's `perfiles` record is fetched.
