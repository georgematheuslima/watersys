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
    
    def verify_product_exists(self, description: str):
        LOGGER.info(f'Verifying if product {description} exists')
        with get_session() as session:
            query = select(ProductModel).filter(ProductModel.descricao == description)
            result = session.execute(query)
            existing_product = result.scalars().unique().one_or_none()
            if existing_product is not None:
                raise ProductAlreadyRegistered
