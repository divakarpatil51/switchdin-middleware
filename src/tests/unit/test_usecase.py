from unittest import mock

import pytest

from src.middleware.domain import models
from src.middleware.interfaces.api.v1.site.serializers import requests
from src.middleware.services import uow, usecase


class FakeRepository:
    def __init__(self):
        self._sites = list()

    def add(self, site: models.Site):
        self._sites.append(site)

    def get(self, reference: int) -> models.Site | None:
        return next((b for b in self._sites if b.id == reference), None)

    def get_by_nmi(self, nmi: str) -> models.Site | None:
        return next((b for b in self._sites if b.nmi == nmi), None)

    def list(self):
        return list(self._sites)


class FakeUnitOfWork(uow.AbstractUoW):
    def __init__(self):
        self.sites = FakeRepository()
        self.committed = False

    def __enter__(self):
        pass

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


async def test_site_creation(anyio_backend):
    uow = FakeUnitOfWork()

    await usecase.create_site(
        requests.SiteCreationRequest(nmi="1234544444"),
        uow,
    )

    assert len(uow.sites.list()) == 1


@mock.patch("middleware.vendors.network_operator_client.register_resource")
async def test_resource_registration(nw_operator_mock, anyio_backend):
    uow = FakeUnitOfWork()

    nmi = "1234544444"

    await usecase.create_site(
        requests.SiteCreationRequest(nmi=nmi),
        uow,
    )

    req = requests.EnergyResourceRegistrationRequest(
        serial_number="1234544444",
        inverter_make="make",
        inverter_model="model",
        generation_capacity_in_kw=1000,
    )
    await usecase.register_resource(nmi, req, uow)

    site = uow.sites.get_by_nmi(nmi)
    assert len(site.energy_resources) == 1

    expected_resource = site.energy_resources.pop()
    assert expected_resource.serial_number == req.serial_number

    nw_operator_mock.assert_called_once_with(req)


async def test_resource_registration_raises_exception_if_site_not_present(
    anyio_backend,
):
    uow = FakeUnitOfWork()

    req = requests.EnergyResourceRegistrationRequest(
        serial_number="1234544444",
        inverter_make="make",
        inverter_model="model",
        generation_capacity_in_kw=1000,
    )
    with pytest.raises(usecase.SiteNotFound):
        await usecase.register_resource("test", req, uow)
