from fastapi import APIRouter

from middleware.interfaces.api.v1 import route as v1_route

router = APIRouter(prefix="/api")
router.include_router(router=v1_route.router, prefix="/v1", tags=["Site"])
