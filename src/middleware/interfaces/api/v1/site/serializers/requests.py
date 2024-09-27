import datetime as dt
import decimal as d

import pydantic as pd
from fastapi import exceptions as fa_ex


class SiteCreationRequest(pd.BaseModel):
    nmi: str

    @pd.field_validator("nmi")
    def validate_nmi(cls, value: str) -> str:
        if len(value) != 10:
            raise fa_ex.ValidationException("Site nmi should be of length 10")
        return value


class EnergyResourceRegistrationRequest(pd.BaseModel):
    serial_number: str
    inverter_make: str
    inverter_model: str
    generation_capacity_in_kw: d.Decimal


class ExportLimitControlRequest(pd.BaseModel):
    site_nmi: str
    start_time: dt.datetime
    end_time: dt.datetime
    export_limit_in_watts: d.Decimal
