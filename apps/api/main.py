from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import UUID

import uvicorn
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from packages.companies.repository import create_company, list_companies
from packages.companies.schemas import CompanyCreate, CompanyRead
from packages.enrichment.service import enrich_company
from packages.icp.repository import create_icp, list_icps
from packages.icp.schemas import ICPCreate, ICPRead
from packages.imports.company_importer import import_companies_from_excel
from packages.organizations.repository import create_organization, create_workspace, list_organizations
from packages.organizations.schemas import (
    OrganizationCreate,
    OrganizationRead,
    WorkspaceCreate,
    WorkspaceRead,
)
from packages.shared.database import get_session

app = FastAPI(title="Sales Intelligence Platform", version="0.1.0")
WEB_ROOT = Path(__file__).resolve().parents[1] / "web"


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/organizations", response_model=OrganizationRead, status_code=201)
def create_organization_endpoint(
    payload: OrganizationCreate,
    session: Session = Depends(get_session),
):
    return create_organization(session, payload)


@app.get("/api/organizations", response_model=list[OrganizationRead])
def list_organizations_endpoint(session: Session = Depends(get_session)):
    return list_organizations(session)


@app.post("/api/workspaces", response_model=WorkspaceRead, status_code=201)
def create_workspace_endpoint(payload: WorkspaceCreate, session: Session = Depends(get_session)):
    return create_workspace(session, payload)


@app.post("/api/companies", response_model=CompanyRead, status_code=201)
def create_company_endpoint(payload: CompanyCreate, session: Session = Depends(get_session)):
    return create_company(session, payload)


@app.get("/api/companies", response_model=list[CompanyRead])
def list_companies_endpoint(organization_id: UUID, session: Session = Depends(get_session)):
    return list_companies(session, organization_id)


@app.post("/api/icps", response_model=ICPRead, status_code=201)
def create_icp_endpoint(payload: ICPCreate, session: Session = Depends(get_session)):
    return create_icp(session, payload)


@app.get("/api/icps", response_model=list[ICPRead])
def list_icps_endpoint(organization_id: UUID, session: Session = Depends(get_session)):
    return list_icps(session, organization_id)


@app.post("/api/imports/companies")
async def import_companies_endpoint(
    organization_id: UUID,
    workspace_id: UUID | None = None,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    suffix = Path(file.filename or "companies.xlsx").suffix or ".xlsx"
    with NamedTemporaryFile(suffix=suffix, delete=True) as temporary:
        temporary.write(await file.read())
        temporary.flush()
        return import_companies_from_excel(session, organization_id, Path(temporary.name), workspace_id)


@app.post("/api/enrichment/companies/{company_id}/simulate", response_model=CompanyRead)
async def simulate_company_enrichment_endpoint(
    company_id: UUID,
    organization_id: UUID,
    session: Session = Depends(get_session),
):
    try:
        return await enrich_company(session, organization_id, company_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


def run() -> None:
    from packages.shared.config import settings

    uvicorn.run("apps.api.main:app", host=settings.app_host, port=settings.app_port, reload=False)


app.mount("/", StaticFiles(directory=WEB_ROOT, html=True), name="web")


if __name__ == "__main__":
    run()
