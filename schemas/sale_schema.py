from pydantic import BaseModel
from datetime import date

class SaleBase(BaseModel):
    quantity: int
    total_amount: float
    purchase_date: date

class SaleCreate(SaleBase):
    product_id: int
    cpf: int

class Sale(SaleBase):
    id: int

    class Config:
        orm_mode = True
