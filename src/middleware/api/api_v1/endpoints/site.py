from fastapi import APIRouter, BackgroundTasks

from src.middleware.api import deps
from src.middleware.schemas.site import (
    SitesExportLimitRequest,
)
from src.middleware.services import site_service

router = APIRouter()


@router.patch("/export-limit")
async def update_export_limit(
    *,
    session: deps.SessionDep,
    cache: deps.CacheDep,
    request: SitesExportLimitRequest,
    background_tasks: BackgroundTasks
) -> dict[str, str]:
    # TODO: try to use celery instead of background_tasks
    background_tasks.add_task(site_service.update_export_limit, session, cache, request)
    return {"message": "Export limit updation started in background successfully"}
