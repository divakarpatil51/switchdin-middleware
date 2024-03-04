from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, validator
from decimal import Decimal


class EnergyResource(BaseModel):
    serial_number: str
    inverter_make: str
    inverter_model: str
    generation_capacity: Decimal


class EnergyResourceRegistrationRequest(EnergyResource):
    site_nmi: str

    @validator("site_nmi")
    def validate_site_nmi(cls, v, *, values, **kwargs) -> str:
        if len(v) != 10:
            raise RequestValidationError("Site nmi should be of length 10")
        return v


class EnergyResourceExportLimitResponse(BaseModel):
    export_limit: Decimal
