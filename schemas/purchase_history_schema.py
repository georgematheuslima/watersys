from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PurchaseHistorySchema(BaseModel):
    id: Optional[int] = None
    purchased_date: datetime = None
    customer: int

    class Config:
        from_attributes = True
