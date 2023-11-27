from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from core.configs import settings
from models.purchase_history_model import PurchaseHistoryModel


class UserModel(settings.DBBaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    email = Column(String(256), index=True, nullable=False, unique=True)
    phone_number = Column(String(10), index=True, nullable=False, unique=True)
    location = Column(String(256), nullable=True)
    is_admin = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    passwd = Column(String(256), nullable=False)
    purchases = relationship(
        PurchaseHistoryModel,
        cascade='all,delete-orphan',
        back_populates='customer',
        uselist=True,
        lazy='joined'
    )
