import datetime
import json

from fastapi.exceptions import RequestValidationError, HTTPException
from sqlalchemy.orm import Session
from redis import Redis

from src.middleware.models import models
from src.middleware.schemas.energy_resource import (
    EnergyResource,
    EnergyResourceRegistrationRequest,
    EnergyResourceExportLimitResponse,
)
from src.middleware.vendors.network_operator import service as nw_operator_service


def register_resource(
    session: Session, registration_request: EnergyResourceRegistrationRequest
) -> EnergyResource:

    energy_resource = (
        session.query(models.EnergyResource)
        .filter_by(serial_number=registration_request.serial_number)
        .first()
    )

    if energy_resource:
        raise RequestValidationError("Energy resource already registered")

    site = (
        session.query(models.Site).filter_by(nmi=registration_request.site_nmi).first()
    )
    if not site:
        site = models.Site(nmi=registration_request.site_nmi)

    site.energy_resources.append(
        models.EnergyResource(
            serial_number=registration_request.serial_number,
            inverter_make=registration_request.inverter_make,
            inverter_model=registration_request.inverter_model,
            generation_capacity=registration_request.generation_capacity,
        )
    )

    nw_operator_service.register_resource(registration_request)

    session.add(site)
    session.commit()

    return registration_request


def get_resources(session: Session, nmi: str) -> list[EnergyResource]:
    resources = session.query(models.EnergyResource)
    if nmi:
        resources = resources.join(models.Site).filter_by(nmi=nmi)

    return resources


def get_export_limit_for_resource(session: Session, cache: Redis, serial_number: str):
    if _resource := cache.get(f"der_{serial_number}"):
        data = json.loads(_resource)
        if (
            datetime.datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S")
            < datetime.datetime.now()
        ):
            return EnergyResourceExportLimitResponse(
                export_limit=_resource["resource_export_limit"]
            )

    _resource = (
        session.query(models.EnergyResource.generation_capacity)
        .filter_by(serial_number=serial_number)
        .first()
    )
    if not _resource:
        raise HTTPException(
            status_code=404,
            detail="Energy resource not found with given serial number",
        )
    return EnergyResourceExportLimitResponse(export_limit=_resource.generation_capacity)
