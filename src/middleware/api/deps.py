from typing import Annotated

from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session
from redis import Redis

from src.middleware.db import engine
from src.middleware.core import config


def get_cache() -> Redis:
    return Redis(host=config.settings.REDIS_HOST, port=config.settings.REDIS_PORT)


def get_db() -> Generator:
    with Session(engine.engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
CacheDep = Annotated[Redis, Depends(get_cache)]
