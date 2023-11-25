from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings

from models.address_model import AddressModel

class ClientModel(settings.DBBaseModel):
    __tablename__ = 'clients'
    id = Column(Integer, name='IDCLIENT', primary_key=True, autoincrement=True)
    client_first_name = Column(String(70), name='FIRST_NAME', nullable=False)
    client_last_name = Column(String(70), name='LAST_NAME', nullable=False)    
    cpf = Column(String(11), name='CPF', nullable=False)
    address_id = Column(Integer, ForeignKey('address.IDADDRESS'))
    phone_number = Column(String(12), name='PHONE',nullable=False)
    email = Column(String(70), name='EMAIL',nullable=False)

    address = relationship(AddressModel, backref='clients')
