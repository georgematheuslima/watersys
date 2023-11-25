from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    id: int
    descricao: str
    unidade_idunidade: int
    valor_compra: Optional[float]
    valor_venda: Optional[float]
    quantidade: int
