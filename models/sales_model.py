from sqlalchemy import Column, Integer, Float, Date, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship
from core.configs import settings

from models.products_model import ProductModel

class SaleModel(settings.DBBaseModel):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, name='QUANTITY',nullable=False)
    total_amount = Column(Float, name='AMOUNT', nullable=False)
    purchase_date = Column(Date, name='PURCHASE_DATE', nullable=False)
    returnable = Column(Boolean, name='RETURNABLE', nullable=False)
    product_id = Column(Integer, ForeignKey("products.IDPRODUTO"))
    product = relationship("ProductModel", back_populates="sales")

    cpf = Column(String, ForeignKey("clients.cpf"))

    customer = relationship("ClientModel", back_populates="sales")
    ProductModel.sales = relationship("SaleModel", back_populates="product")
