import datetime
import json

from redis import Redis
from sqlalchemy.orm import Session

from src.middleware import utils
from src.middleware.models import models
from src.middleware.schemas.site import SitesExportLimitRequest


def update_export_limit(
    session: Session, cache: Redis, request: SitesExportLimitRequest
) -> None:

    sites: list[models.Site] = session.query(models.Site).filter(
        models.Site.nmi.in_(request.data.keys())
    )

    for site in sites:
        _site_data = request.data.get(site.nmi)
        export_limit_in_kw = utils.watts_to_kilowatts(_site_data.export_limit)

        resources: list[models.EnergyResource] = site.energy_resources
        total_site_generation_capacity = sum(
            resource.generation_capacity for resource in resources
        )
        for resource in resources:
            proportion = resource.generation_capacity / total_site_generation_capacity
            resource_export_limit = proportion * export_limit_in_kw

            data = {
                "start_time": _site_data.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "resource_export_limit": str(resource_export_limit),
            }

            expire_at = _site_data.end_time - datetime.datetime.now()
            cache.set(f"der_{resource.serial_number}", json.dumps(data), ex=expire_at)

        export_limit = models.ExportLimit()
        export_limit.start_time = _site_data.start_time
        export_limit.end_time = _site_data.end_time
        export_limit.export_limit = _site_data.export_limit_in_kw
        export_limit.site_id = site.id
        session.add(export_limit)

    session.commit()
