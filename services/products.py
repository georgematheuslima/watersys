import logging
import traceback

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.future import select
from core.deps import get_session

from models.products import ProductModel
from validation.product import ProductValidation
from exceptions.product import ProductAlreadyRegistered
LOGGER = logging.getLogger("sLogger")


class ProductService:

    async def validate_product_exists(self, description: str, db: AsyncSession = Depends(get_session)):
        async with db as session:
            query = select(ProductModel).filter(ProductModel.descricao == description)
            result = await session.execute(query)
            existing_product = result.scalars().unique().one_or_none()
            if existing_product != None:
                raise ProductAlreadyRegistered

    async def create_new_product(self, product: ProductModel, db: AsyncSession = Depends(get_session)):
        LOGGER.info(f'Processing create new product: {product.descricao}')

        ProductValidation.validate_product_model(product.model_dump())
        self.validate_product_exists(description=product.descricao)

        new_product = ProductModel(
            description = product.descricao,
            unity_id = product.unidade_idunidade,
            purchase_price = product.valor_compra,
            sale_price = product.valor_venda,
            units = product.unidades
        )
        async with db as session:
            try:
                session.add(new_product)
                await session.commit()
                
                LOGGER.info(F'New product was created!')
                return new_product
            except IntegrityError as exc:
                LOGGER.error(traceback.format_exc, exc)
                LOGGER.info(f'An integrity error was returned: {exc}')
            except OperationalError as exc:
                LOGGER.error(traceback.format_exc, exc)
                LOGGER.info(f'An error occurred at DBconnect')