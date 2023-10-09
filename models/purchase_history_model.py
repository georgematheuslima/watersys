from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.configs import settings
from sqlalchemy.sql import func


class PurchaseHistoryModel(settings.DBBaseModel):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True, autoincrement=True)
    purchased_date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    customer = relationship(
        'UserModel', back_populates='purchases', lazy='joined')
