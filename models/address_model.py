import logging

from sqlalchemy import Column, Integer, String
from core.configs import settings

LOGGER = logging.getLogger('sLogger')


class AddressModel(settings.DBBaseModel):
    __tablename__ = 'address'

    id = Column(Integer, name='IDADDRESS', primary_key=True, autoincrement=True)
    address = Column(String(255), name='ADDRESS', nullable=False)
    type = Column(String(50), name='TYPE', nullable=False)
    state = Column(String(50), name='STATE', nullable=False)
    abbreviation = Column(String(10), name='ABBREVIATION', nullable=False)
    city = Column(String(50), name='CITY', nullable=False)
    neighborhood = Column(String(50), name='NEIGHBORHOOD', nullable=True)
    reference_point = Column(String(255), name='REFERENCE_POINT', nullable=True)