import datetime as dt
import decimal as d
import random
import string

import pytest
from fastapi import testclient

from src.middleware.interfaces.api.v1.site.serializers import requests
from src.middleware.interfaces.tasks import update_site_export_limit

BASE_URL = "/api/v1"


def generate_random_data(size=10) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(size))


def create_site(api_client: testclient.TestClient, nmi: str):
    response = api_client.post(
        f"{BASE_URL}/sites",
        json={
            "nmi": nmi,
        },
    )
    assert response.status_code == 201
    assert response.json() == f"Inserted site with nmi {nmi} successfully"


def register_resource(
    api_client: testclient.TestClient,
    nmi: str,
    serial_number: str,
):
    resource = {
        "serial_number": serial_number,
        "inverter_make": "str",
        "inverter_model": "str",
        "generation_capacity_in_kw": "101.2",
    }

    response = api_client.post(
        f"{BASE_URL}/sites/{nmi}/energy_resources",
        json=resource,
    )
    assert response.status_code == 200
    assert (
        response.json()
        == f"Resource with serial number {serial_number} registered successfully"
    )


def get_resources_for_site_nmi(api_client: testclient.TestClient, nmi: str):
    response = api_client.get(f"{BASE_URL}/sites/{nmi}/energy_resources")
    assert response.status_code == 200
    return response.json()


@pytest.mark.usefixtures("sqllite_db")
def test_update_site_export_limit_task(api_client: testclient.TestClient):
    nmi = generate_random_data()
    create_site(api_client, nmi)
    register_resource(api_client, nmi, generate_random_data())
    register_resource(api_client, nmi, generate_random_data())

    update_site_export_limit.update_site_export_limit(
        site_export_limit_control=requests.ExportLimitControlRequest(
            site_nmi=nmi,
            start_time=dt.datetime.now(),
            end_time=dt.datetime.now(),
            export_limit_in_watts=d.Decimal(1000000),
        )
    )

    resources = get_resources_for_site_nmi(api_client, nmi)

    assert d.Decimal(resources[0]["current_export_limit_in_kw"]) == d.Decimal(500)
    assert d.Decimal(resources[1]["current_export_limit_in_kw"]) == d.Decimal(500)
