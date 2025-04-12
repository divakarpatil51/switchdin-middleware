from fastapi import FastAPI

from middleware.adapters import orm
from middleware.core import celery_config
from middleware.interfaces.api import route


orm.start_mappers()

app = FastAPI()
app.include_router(router=route.router)
celery_app = celery_config.init()
