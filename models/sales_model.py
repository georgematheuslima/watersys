from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings

class SaleModel(settings.DBBaseModel):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, name='QUANTITY',nullable=False)
    total_amount = Column(Float, name='AMOUNT', nullable=False)
    purchase_date = Column(Date, name='PURCHASE_DATE', nullable=False)

    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="sales")

    customer_id = Column(Integer, ForeignKey("clients.id"))
    customer = relationship("Client", back_populates="sales")
