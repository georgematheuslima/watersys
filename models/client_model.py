from sqlalchemy import Table, Column, Integer, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.address_model import AddressModel
from models.sales_model import SaleModel
from core.configs import settings

Base = declarative_base()

class ClientModel(settings.DBBaseModel):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_first_name = Column(String(70), name='FIRST_NAME', nullable=False)
    client_last_name = Column(String(70), name='LAST_NAME', nullable=False)    
    cpf = Column(String(11), name='cpf', nullable=False, unique=True)
    address_id = Column(Integer, ForeignKey('address.IDADDRESS'))
    phone_number = Column(String(12), name='PHONE', nullable=False)
    email = Column(String(70), name='EMAIL', nullable=False)

    client_address = relationship(AddressModel, backref='client')
    sales = relationship(SaleModel, back_populates="customer")