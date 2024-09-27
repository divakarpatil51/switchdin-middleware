import sqlalchemy as sa
from sqlalchemy import orm

from middleware.domain import models

mapper_registry = orm.registry()


meter_reading = sa.Table(
    "meter_reading",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("reading_time", sa.DateTime()),
    sa.Column("reading_value", sa.DECIMAL()),
    sa.Column("energy_resource_id", sa.ForeignKey("energy_resource.id")),
)

energy_resource = sa.Table(
    "energy_resource",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("serial_number", sa.String(255)),
    sa.Column("inverter_make", sa.String(255)),
    sa.Column("inverter_model", sa.String(255)),
    sa.Column("generation_capacity_in_kw", sa.DECIMAL()),
    sa.Column("current_export_limit_in_kw", sa.DECIMAL()),
    sa.UniqueConstraint("serial_number"),
    sa.Column("site_id", sa.ForeignKey("site.id")),
)

export_limit_control = sa.Table(
    "export_limit_control",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("start_time", sa.DateTime()),
    sa.Column("end_time", sa.DateTime()),
    sa.Column("export_limit_in_watts", sa.DECIMAL()),
    sa.Column("site_id", sa.ForeignKey("site.id")),
)

site = sa.Table(
    "site",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("nmi", sa.String(255)),
    sa.UniqueConstraint("nmi"),
)


def start_mappers():
    mapper_registry.map_imperatively(
        models.EnergyResource,
        energy_resource,
        properties={
            "meter_readings": orm.relationship(
                models.MeterReading,
                backref="energy_resource",
                order_by=meter_reading.c.id,
            )
        },
    )

    mapper_registry.map_imperatively(
        models.Site,
        site,
        properties={
            "energy_resources": orm.relationship(
                models.EnergyResource,
                backref="site",
                order_by=energy_resource.c.id,
                collection_class=set,
            ),
            "export_limit_controls": orm.relationship(
                models.ExportLimitControl,
                backref="site",
                order_by=export_limit_control.c.id,
                collection_class=set,
            ),
        },
    )

    mapper_registry.map_imperatively(
        models.MeterReading,
        meter_reading,
    )

    mapper_registry.map_imperatively(
        models.ExportLimitControl,
        export_limit_control,
    )
