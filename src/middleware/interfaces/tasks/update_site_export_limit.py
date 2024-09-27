import celery as cl 

from middleware.interfaces.api.v1.site.serializers import requests
from middleware.services import uow, usecase


@cl.shared_task
def update_site_export_limit(
    *,
    site_export_limit_control: dict,
):
    req = requests.ExportLimitControlRequest.parse_obj(
        site_export_limit_control,
    )
    _uow = uow.SqlAlchemyUoW(create_scoped_session=True)
    usecase.update_site_export_limit(req, _uow)
