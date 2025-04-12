import dataclasses as dc
import datetime as dt
import decimal as d
from typing_extensions import override

# These are domain models


# This is a Value Object in DDD as it does not have any identity of itself.
# They should be made immutable
@dc.dataclass
class MeterReading:
    reading_time: dt.datetime
    reading_value: d.Decimal


class EnergyResource:
    def __init__(
        self,
        serial_number: str,
        inverter_make: str,
        inverter_model: str,
        generation_capacity_in_kw: d.Decimal,
    ):
        self.serial_number: str = serial_number
        self.inverter_make: str = inverter_make
        self.inverter_model: str = inverter_model
        self.generation_capacity_in_kw: d.Decimal = generation_capacity_in_kw
        self.current_export_limit_in_kw: d.Decimal | None = None

    def update_export_limit(self, new_export_limit: d.Decimal):
        self.current_export_limit_in_kw = new_export_limit

    def __str__(self):
        return (
            f"EnergyResource({self.serial_number=}, {self.inverter_model=},"
            f" {self.inverter_make=}, {self.generation_capacity_in_kw=},"
            f" {self.current_export_limit_in_kw}"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, EnergyResource):
            return False
        return other.serial_number == self.serial_number

    def __hash__(self):
        return hash(self.serial_number)


# This is a Value Object in DDD as it does not have any identity of itself.
# It should be made immutable
class ExportLimitControl:
    def __init__(
        self,
        start_time: dt.datetime,
        end_time: dt.datetime,
        export_limit_in_watts: d.Decimal,
    ):
        self.start_time: dt.datetime = start_time
        self.end_time: dt.datetime = end_time
        self.export_limit_in_watts: d.Decimal = export_limit_in_watts


# Active Record Pattern or Data Mapper Pattern?
# Active Record Pattern is a design pattern that is used to represent the data in the database as objects in the application.
# Data Mapper Pattern is a design pattern that is used to separate the data from the business logic.
# This is Data Mapper Pattern as the domain models are not responsible for their own persistence.
class Site:
    def __init__(self, nmi: str):
        self.nmi: str = nmi
        self.energy_resources: set[EnergyResource] = set()
        self.export_limit_controls: set[ExportLimitControl] = set()

    @override
    def __str__(self) -> str:
        return f"Site(nmi={self.nmi})"

    @override
    def __repr__(self) -> str:
        return f"Site(nmi={self.nmi})"

    @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, Site):
            return False
        return other.nmi == self.nmi

    @override
    def __hash__(self) -> int:
        return hash(self.nmi)

    async def register_resource(self, resource: EnergyResource) -> None:
        self.energy_resources.add(resource)

    def update_resources_export_limit(
        self,
        export_limit_control: ExportLimitControl,
    ) -> None:
        self.export_limit_controls.add(export_limit_control)
        export_limit_in_kw = d.Decimal(
            export_limit_control.export_limit_in_watts / 1000
        )
        site_generation_capacity = sum(
            res.generation_capacity_in_kw for res in self.energy_resources
        )
        for resource in self.energy_resources:
            proportion = d.Decimal(
                resource.generation_capacity_in_kw / site_generation_capacity
            )
            resource_export_limit = proportion * export_limit_in_kw
            resource.current_export_limit_in_kw = resource_export_limit
