from schemas.address_schema import AddressSchema

from pydantic import BaseModel

class ClientSchema(BaseModel):
    id: int
    client_first_name: str
    client_last_name: str
    tax_id: str
    address: AddressSchema
    phone_number: str
    email: str
