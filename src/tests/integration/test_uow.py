import random
import string

import sqlalchemy as sa
from sqlalchemy import orm as sa_orm

from src.middleware.domain import models
from src.middleware.services import uow


def generate_random_data(size=10) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(size))


def test_uow_can_persist_site(session_factory):
    nmi = generate_random_data()
    with uow.SqlAlchemyUoW(session_factory) as _uow:
        _uow.sites.add(models.Site(nmi=nmi))
        _uow.commit()

    session = session_factory()
    resp = list(
        session.execute(
            sa.text("SELECT * FROM site where nmi = :nmi"),
            dict(nmi=nmi),
        )
    )
    assert len(resp) == 1
    assert resp[0][1] == nmi


def insert_site(session: sa_orm.Session, nmi: str):
    session.execute(
        sa.text("INSERT INTO site (nmi) values (:nmi)"),
        dict(nmi=nmi),
    )


async def test_uow_can_add_resource_to_a_site(anyio_backend, session_factory):
    nmi = generate_random_data()
    session: sa_orm.Session = session_factory()
    insert_site(session, nmi)
    session.commit()

    with uow.SqlAlchemyUoW(session_factory) as _uow:
        site = _uow.sites.get_by_nmi(nmi)
        serial_number = generate_random_data()
        await site.register_resource(
            models.EnergyResource(
                serial_number=serial_number,
                inverter_make="make",
                inverter_model="model",
                generation_capacity_in_kw=1000,
            )
        )
        _uow.sites.add(site)
        _uow.commit()

    session = session_factory()
    resp = list(
        session.execute(
            sa.text(
                "SELECT nmi, er.serial_number FROM site "
                "join energy_resource as er on er.site_id = site.id "
                "where nmi = :nmi"
            ),
            dict(nmi=nmi),
        )
    )
    assert len(resp) == 1
    assert resp[0][0] == nmi
    assert resp[0][1] == serial_number
