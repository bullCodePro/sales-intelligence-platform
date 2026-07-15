# Sales Intelligence Platform

MVP para organizar empresas objetivo, contactos y scoring ICP desde una API local con una interfaz web simple.

## Ejecutar

```bash
python3 -m scripts.seed
python3 -m apps.api.server
```

Abrir:

```text
http://127.0.0.1:8000
```

## Endpoints

- `GET /api/health`
- `GET /api/companies`
- `POST /api/companies`
- `GET /api/contacts`
- `POST /api/contacts`
- `GET /api/scores`
- `GET /api/export/companies.csv`

## Estructura

- `apps/api`: servidor HTTP y rutas JSON.
- `apps/web`: dashboard web.
- `packages/companies`: persistencia de cuentas objetivo.
- `packages/contacts`: persistencia de contactos.
- `packages/scoring`: cálculo de ICP.
- `packages/exports`: exportación CSV.
- `packages/shared`: base de datos y utilidades comunes.
