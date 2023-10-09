from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PurchaseHistorySchema(BaseModel):
    id: Optional[int] = None
    purchased_date: datetime = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
