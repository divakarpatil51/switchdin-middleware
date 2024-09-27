import typing as t

import fastapi as fapi
from fastapi import responses

from middleware.interfaces.api.v1.site.serializers import (
    requests,
)
from middleware.interfaces.api.v1.site.serializers import (
    responses as site_responses,
)
from middleware.interfaces.tasks import update_site_export_limit
from middleware.services import uow, usecase

router = fapi.APIRouter()


@router.post("")
async def create_site(
    site_request: requests.SiteCreationRequest,
) -> responses.JSONResponse:
    _uow = uow.SqlAlchemyUoW()
    await usecase.create_site(site_request, _uow)
    return responses.JSONResponse(
        f"Inserted site with nmi {site_request.nmi} successfully",
        status_code=201,
    )


@router.post("/{site_nmi}/energy_resources")
async def register_resource(
    site_nmi: str,
    energy_resource_request: requests.EnergyResourceRegistrationRequest,
) -> responses.JSONResponse:
    _uow = uow.SqlAlchemyUoW()

    await usecase.register_resource(
        site_nmi,
        energy_resource_request,
        _uow,
    )
    return responses.JSONResponse(
        f"Resource with serial number {energy_resource_request.serial_number} "
        "registered successfully"
    )


@router.get("/{site_nmi}/energy_resources")
async def get_site_resources(
    site_nmi: str,
) -> t.Sequence[site_responses.EnergyResourceRegistrationResponse]:
    _uow = uow.SqlAlchemyUoW()
    resources = await usecase.get_resources_for_site_nmi(site_nmi, _uow)
    return resources


@router.post("/export_limits")
async def update_sites_export_limits(
    export_limit_controls: t.Sequence[requests.ExportLimitControlRequest],
) -> responses.JSONResponse:
    tasks = []
    for export_limit_control in export_limit_controls:
        task = update_site_export_limit.delay(
            site_export_limit_control=export_limit_control.dict(),
        )
        tasks.append(task.id)

    return responses.JSONResponse(
        f"Export limit updated successfully: {tasks}",
    )
