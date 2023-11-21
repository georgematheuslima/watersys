from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from core.configs import settings
from sqlalchemy.sql import func


class WarehouseModel(settings.DBBaseModel):
    __tablename__ = 'warehouses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    coordinates = Column(Geometry('POINT'), index=True)
