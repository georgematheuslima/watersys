from pydantic import BaseModel
from datetime import date

class SaleBase(BaseModel):
    quantity: int
    total_amount: float
    purchase_date: date
    returnable: bool

class SaleCreate(SaleBase):
    product_id: int
    cpf: str

class Sale(SaleBase):
    id: int

    class Config:
        from_attributes = True
