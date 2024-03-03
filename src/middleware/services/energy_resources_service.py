from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session

from src.middleware.models import models
from src.middleware.schemas.energy_resource import (
    EnergyResource,
    EnergyResourceRegistrationRequest,
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
