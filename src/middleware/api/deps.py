from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.middleware.db import engine


def get_db() -> Generator:
    with Session(engine.engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
