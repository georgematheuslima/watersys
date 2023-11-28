from schemas.address_schema import AddressSchema
from pydantic import BaseModel

class ClientSchema(BaseModel):
    client_first_name: str
    client_last_name: str
    cpf: str
    address: AddressSchema
    phone_number: str
    email: str

class ClientSchemaReturn(BaseModel):
    id: int
    client_first_name: str
    client_last_name: str
    cpf: str
    address: AddressSchema
    phone_number: str
    email: str