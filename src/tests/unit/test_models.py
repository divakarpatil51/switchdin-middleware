import datetime as dt
from decimal import Decimal

from src.middleware.domain import models


async def test_successful_resource_registration(anyio_backend):
    site = models.Site(nmi="1234567890")

    resource = models.EnergyResource(
        serial_number="1234567890",
        inverter_make="test",
        inverter_model="test",
        generation_capacity_in_kw=Decimal(1),
    )
    await site.register_resource(resource)

    assert len(site.energy_resources) == 1


async def test_add_export_limit_control(anyio_backend):
    site = models.Site(nmi="1234567890")

    resources = [
        models.EnergyResource(
            serial_number="1234567890",
            inverter_make="test",
            inverter_model="test",
            generation_capacity_in_kw=Decimal(1000),
        ),
        models.EnergyResource(
            serial_number="1234567891",
            inverter_make="test",
            inverter_model="test",
            generation_capacity_in_kw=Decimal(3000),
        ),
    ]

    for res in resources:
        await site.register_resource(res)

    control = models.ExportLimitControl(
        start_time=dt.datetime.now(),
        end_time=dt.datetime.now() + dt.timedelta(days=2),
        export_limit_in_watts=Decimal(1500000),
    )
    await site.update_resources_export_limit(export_limit_control=control)

    assert Decimal(resources[0].current_export_limit_in_kw) == 375
    assert Decimal(resources[1].current_export_limit_in_kw) == 1125
