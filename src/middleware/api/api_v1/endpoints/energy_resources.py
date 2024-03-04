from fastapi import APIRouter

from src.middleware.api import deps
from src.middleware.schemas.energy_resource import (
    EnergyResource,
    EnergyResourceExportLimitResponse,
    EnergyResourceRegistrationRequest,
)
from src.middleware.services import energy_resources_service

router = APIRouter()


@router.post("/register", response_model=EnergyResource)
def register_resource(
    *, session: deps.SessionDep, request: EnergyResourceRegistrationRequest
) -> EnergyResource:
    return energy_resources_service.register_resource(session, request)


@router.get("", response_model=list[EnergyResource])
def get_resources(*, session: deps.SessionDep, nmi: str = None) -> list[EnergyResource]:
    return energy_resources_service.get_resources(session=session, nmi=nmi)


@router.get(
    "/{serial_number}/export-limit", response_model=EnergyResourceExportLimitResponse
)
def get_export_limit_for_resource(
    *, session: deps.SessionDep, cache: deps.CacheDep, serial_number: str
) -> EnergyResourceExportLimitResponse:
    return energy_resources_service.get_export_limit_for_resource(
        session, cache, serial_number
    )
