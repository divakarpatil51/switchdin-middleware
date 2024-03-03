from fastapi import FastAPI

from src.middleware.api.api_v1 import api
from src.middleware.core import config

app = FastAPI(title=config.settings.PROJECT_NAME)

app.include_router(api.router)
