import typing as t

from middleware.domain import models
from middleware.interfaces.api.v1.site.serializers import requests, responses
from middleware.services import uow
from middleware.vendors import network_operator_client


class SiteNotFound(Exception):
    pass


async def create_site(
    site_request: requests.SiteCreationRequest,
    uow: uow.AbstractUoW,
):
    with uow:
        site = models.Site(nmi=site_request.nmi)
        uow.sites.add(site)
        uow.commit()


async def register_resource(
    site_nmi: str,
    request: requests.EnergyResourceRegistrationRequest,
    uow: uow.AbstractUoW,
):
    with uow:
        site: models.Site | None = uow.sites.get_by_nmi(site_nmi)
        if not site:
            raise SiteNotFound(f"Site with nmi {site_nmi} not found")

        await site.register_resource(
            models.EnergyResource(
                serial_number=request.serial_number,
                inverter_make=request.inverter_make,
                inverter_model=request.inverter_model,
                generation_capacity_in_kw=request.generation_capacity_in_kw,
            )
        )

        await network_operator_client.register_resource(request)
        uow.sites.add(site)
        uow.commit()


async def get_resources_for_site_nmi(
    site_nmi: str,
    uow: uow.AbstractUoW,
) -> t.Sequence[responses.EnergyResourceRegistrationResponse]:
    with uow:
        site: models.Site | None = uow.sites.get_by_nmi(site_nmi)
        if not site:
            raise SiteNotFound(f"Site with nmi {site_nmi} not found")

        resources = [
            responses.EnergyResourceRegistrationResponse(
                serial_number=res.serial_number,
                inverter_make=res.inverter_make,
                inverter_model=res.inverter_model,
                generation_capacity_in_kw=res.generation_capacity_in_kw,
                current_export_limit_in_kw=res.current_export_limit_in_kw,
            )
            for res in site.energy_resources
        ]

        return resources


def update_site_export_limit(
    export_limit_control_req: requests.ExportLimitControlRequest,
    uow: uow.AbstractUoW,
) -> None:
    with uow:
        site: models.Site | None = uow.sites.get_by_nmi(
            export_limit_control_req.site_nmi,
        )
        if not site:
            raise SiteNotFound(
                f"Site with nmi {export_limit_control_req.site_nmi} not found"
            )

        export_limit_control = models.ExportLimitControl(
            export_limit_control_req.start_time,
            export_limit_control_req.end_time,
            export_limit_control_req.export_limit_in_watts,
        )
        site.update_resources_export_limit(export_limit_control)
        uow.sites.add(site)
        uow.commit()
