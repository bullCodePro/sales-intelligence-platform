# Sales Intelligence Platform

Plataforma genérica y multiempresa de inteligencia comercial y prospección B2B.

El dominio principal es reusable para distintos clientes, países, sectores e ICPs. Los casos concretos viven como datos de `Organization`, `Workspace`, `ICP`, campañas o importaciones; no como lógica fija del código.

## Ejecutar

```bash
uv sync
docker compose up -d postgres redis
uv run alembic upgrade head
uv run sales-api
```

Abrir:

```text
http://127.0.0.1:8000
```

## Endpoints

- `GET /api/health`
- `POST /api/organizations`
- `GET /api/organizations`
- `POST /api/companies`
- `GET /api/companies?organization_id=...`
- `POST /api/icps`
- `GET /api/icps?organization_id=...`
- `POST /api/imports/companies`
- `POST /api/enrichment/companies/{company_id}/simulate`

## Estructura

- `apps/api`: API FastAPI.
- `apps/web`: frontend futuro.
- `apps/worker`: jobs de importación, enriquecimiento y campañas.
- `packages/organizations`: organizaciones y workspaces.
- `packages/companies`: empresas, aliases y datos firmográficos.
- `packages/contacts`: contactos y roles.
- `packages/icp`: perfiles ideales y reglas.
- `packages/enrichment`: proveedores simulados y contratos de integración.
- `packages/imports`: importación Excel/CSV.
- `packages/scoring`: cálculo de score.
- `packages/shared`: configuración, base declarativa y sesión SQLAlchemy.

## Principios

- Todas las entidades de negocio incluyen `organization_id`.
- No se inventan personas, emails ni cargos: los proveedores simulados solo generan datos marcados como simulados.
- Cada dato enriquecido debe guardar fuente, fecha y confianza.
- Los proveedores externos se conectan por interfaces, no por dependencias directas del dominio.
