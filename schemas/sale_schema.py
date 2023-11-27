from pydantic import BaseModel
from datetime import date

class SaleBase(BaseModel):
    quantity: int
    returnable: bool

class SaleCreate(SaleBase):
    product_id: int
    cpf: str

class SaleResponse(BaseModel):
    purchase_date: date
    total_amount: float
    id: int

    class Config:
        from_attributes = True

class SaleAllInfo(BaseModel):
    quantity: int
    returnable: bool
    purchase_date: date
    product_id: int
    cpf: str
    total_amount: float
    id: int

    class Config:
        from_attributes = True
