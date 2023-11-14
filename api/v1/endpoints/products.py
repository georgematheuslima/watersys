import logging
import traceback

from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError


from services.products import ProductService
from models.products import ProductModel
from schemas.product import ProductSchema
from validation.product import ProductValidation
from exceptions.validations import FieldWithValueLessThanZero
from exceptions.product import ProductAlreadyRegistered
from exceptions.general_exceptions import ServerException
from utils.system_messages.system_messages import (FIELD_VALUE_LESS_THAN_ZERO)
from utils.system_messages.product.product_messages import(PRODUCT_ALREADY_REGISTERED)

from core.deps import get_session

router = APIRouter()
LOGGER = logging.getLogger('sLogger')


@router.post('/product', status_code=HTTPStatus.CREATED, response_model=ProductSchema)
async def create_new_product(product: ProductSchema, db: AsyncSession = Depends(get_session)):
    try:
        LOGGER.info(f'Starting create new product: {product}')

        ProductValidation().validate_product_model(product.model_dump())

        new_product = ProductModel(
            descricao=product.descricao,
            unidade_idunidade=product.unidade_idunidade,
            valor_compra=product.valor_compra,
            valor_venda=product.valor_venda,
            quantidade=product.quantidade
        )

        async with db as session:
            try:
                session.add(new_product)
                await session.commit()
                LOGGER.info('New product was created!')
                return product
            except IntegrityError as exc:
                LOGGER.error(traceback.format_exc(), exc)
                return JSONResponse(content={"message": 'An integrity error occurred'}, status_code=HTTPStatus.CONFLICT)
            except OperationalError as exc:
                LOGGER.error(traceback.format_exc(), exc)
                return JSONResponse(content={"message": 'An error occurred at DB connect'}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    except FieldWithValueLessThanZero as exc:
        return JSONResponse(content={"message": 'Field value less than zero'}, status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    except ProductAlreadyRegistered as exc:
        return JSONResponse(content={"message": 'Product already registered'}, status_code=HTTPStatus.CONFLICT)
    except HTTPException as http_exc:
        LOGGER.error(traceback.format_exc())
        return JSONResponse(content={"message": http_exc.detail}, status_code=http_exc.status_code)
    except ServerException as exc:
        LOGGER.error(traceback.format_exc())
        return JSONResponse(content={"message": exc.message}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    except Exception as exc:
        LOGGER.error(traceback.format_exc())
        return JSONResponse(content={"message": 'An error occurred'}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

@router.get('/product/{id}', status_code=HTTPStatus.OK, response_model=ProductSchema)
async def get_product_by_id(product_id: int):
    try:
        LOGGER.info(f'Getting product by id: {product_id}')
        response = await ProductService.get_product_id(product_id=product_id)
        return JSONResponse(content=response, status_code=HTTPStatus.OK)
    except:
        pass