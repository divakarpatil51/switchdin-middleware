from sqlalchemy import DECIMAL, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Site(Base):
    __tablename__ = "site"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nmi = Column(String(10), unique=True)

    energy_resources = relationship("EnergyResource", uselist=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class EnergyResource(Base):
    __tablename__ = "energy_resource"

    id = Column(Integer, primary_key=True, autoincrement=True)
    serial_number = Column(String(10), unique=True)
    inverter_make = Column(String())
    inverter_model = Column(String())
    generation_capacity = Column(DECIMAL())

    site_id = Column(Integer, ForeignKey("site.id"), primary_key=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
