import decimal as d
import random
import string

import pytest
from fastapi import exceptions as fa_ex
from fastapi import testclient

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


@pytest.mark.usefixtures("sqllite_db")
def test_api_create_site(api_client: testclient.TestClient):
    create_site(api_client, generate_random_data(10))


@pytest.mark.usefixtures("sqllite_db")
def test_exception_raised_for_invalid_nmi(api_client: testclient.TestClient):
    with pytest.raises(
        fa_ex.ValidationException, match="Site nmi should be of length 10"
    ):
        api_client.post(
            f"{BASE_URL}/sites",
            json={
                "nmi": "test",
            },
        )


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
def test_api_register_resource(api_client: testclient.TestClient):
    nmi = generate_random_data()
    create_site(api_client, nmi)

    register_resource(api_client, nmi, generate_random_data())


@pytest.mark.usefixtures("sqllite_db")
def test_api_update_resource_export_limits(api_client: testclient.TestClient):
    nmi = generate_random_data()
    create_site(api_client, nmi)

    resource_serial_number = generate_random_data()
    register_resource(api_client, nmi, resource_serial_number)
    resource_serial_number_1 = generate_random_data()
    register_resource(api_client, nmi, resource_serial_number_1)

    export_limit = [
        {
            "site_nmi": nmi,
            "start_time": "2020-01-10",
            "end_time": "2020-01-13",
            "export_limit_in_watts": "1000000",
        }
    ]
    response = api_client.post(
        f"{BASE_URL}/sites/export_limits",
        json=export_limit,
    )
    assert response.status_code == 200
    assert response.json() == "Export limit updated successfully"

    resources = get_resources_for_site_nmi(api_client, nmi)

    assert d.Decimal(
        resources[0]["current_export_limit_in_kw"],
    ) == d.Decimal(500)
    assert d.Decimal(
        resources[1]["current_export_limit_in_kw"],
    ) == d.Decimal(500)
