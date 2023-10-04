from pydantic import BaseModel, Field

class UserDataModel(BaseModel):
    name: str = Field(..., alias='Nome completo')
    address: str = Field(..., alias='Endereço')
    phone_number: str = Field(..., alias='Telefone')