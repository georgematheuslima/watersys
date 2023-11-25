from pydantic import BaseModel

class AddressSchema(BaseModel):
    id: int
    address: str
    type: str
    state: str
    abbreviation: str
    city: str
    neighborhood: str
    reference_point: str