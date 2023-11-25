from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from schemas.purchase_history_schema import PurchaseHistorySchema


class UserSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    is_admin: bool = False

    class Config:
        from_attributes: True


class UserSchemaCreate(UserSchemaBase):
    passwd: str


class UserSchemaPurchases(UserSchemaBase):
    purchases: Optional[List[PurchaseHistorySchema]]


class UserSchemaUp(UserSchemaBase):
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    passwd: Optional[str] = None
    phone_number: Optional[str] = None
    is_admin: Optional[bool] = None
