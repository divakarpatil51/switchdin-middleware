import decimal as d

import pydantic as pd


class EnergyResourceRegistrationResponse(pd.BaseModel):
    serial_number: str
    inverter_make: str
    inverter_model: str
    generation_capacity_in_kw: d.Decimal
    current_export_limit_in_kw: d.Decimal | None
