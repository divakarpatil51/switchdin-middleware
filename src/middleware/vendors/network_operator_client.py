from middleware.interfaces.api.v1.site.serializers import requests


async def register_resource(
    resource_registration_request: requests.EnergyResourceRegistrationRequest,
) -> None: ...
