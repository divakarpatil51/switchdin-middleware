import datetime
from decimal import Decimal

from pydantic import BaseModel


class Site(BaseModel):
    nmi: str


class SiteExportLimitRequest(BaseModel):
    start_time: datetime.datetime
    end_time: datetime.datetime
    export_limit: Decimal


class SitesExportLimitRequest(BaseModel):
    data: dict[str, SiteExportLimitRequest]
