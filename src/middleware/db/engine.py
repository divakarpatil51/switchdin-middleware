from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.middleware.core import config

engine = create_engine(url=str(config.settings.SQLALCHEMY_DATABASE_URI))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
