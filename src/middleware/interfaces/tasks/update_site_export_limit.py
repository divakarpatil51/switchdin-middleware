import celery as cl

from middleware.interfaces.api.v1.site.serializers import requests
from middleware.services import uow, usecase
import typing as t


@cl.shared_task
def update_site_export_limit(
    *,
    site_export_limit_control: dict[str, t.Any],
):
    req = requests.ExportLimitControlRequest.model_validate(
        site_export_limit_control,
    )
    _uow = uow.SqlAlchemyUoW(create_scoped_session=True)
    usecase.update_site_export_limit(req, _uow)
