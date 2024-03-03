from fastapi import APIRouter

from src.middleware.api.api_v1.endpoints import energy_resources, site

router = APIRouter()

router.include_router(
    energy_resources.router, prefix="/energy-resources", tags=["Energy Resources"]
)
router.include_router(site.router, prefix="/site", tags=["Site"])
