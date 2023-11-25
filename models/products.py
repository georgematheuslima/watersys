from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from core.configs import settings



class ProductModel(settings.DBBaseModel):
    __tablename__ = 'produtos'
    id = Column(Integer, name='IDPRODUTO', primary_key=True, autoincrement=True)
    descricao = Column(String(100), name='DESCRICAO', nullable=True)
    unidade_idunidade = Column(Integer, name='UNIDADES_IDUNIDADE', nullable=False)
    valor_compra = Column(Float, name='VALORCOMPRA', nullable=True)
    valor_venda = Column(Float, name='VALORVENDA', nullable=True)
    unidades = relationship("UnidadeModel", backref="produtos")