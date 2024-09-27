from fastapi import APIRouter

from middleware.interfaces.api.v1.site import route as site_route

router = APIRouter()
router.include_router(router=site_route.router, prefix="/sites", tags=["Site"])
