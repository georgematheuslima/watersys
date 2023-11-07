import logging
import traceback

from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from services.products import ProductService
from models.products import ProductModel
from exceptions.validations import FieldWithValueLessThanZero
from exceptions.product import ProductAlreadyRegistered
from exceptions.general_exceptions import ServerException
from utils.system_messages.system_messages import (FIELD_VALUE_LESS_THAN_ZERO)
from utils.system_messages.product.product_messages import(PRODUCT_ALREADY_REGISTERED)

from core.deps import get_session

router = APIRouter()
LOGGER = logging.getLogger('sLogger')


@router.post('/product',status_code=HTTPStatus.CREATED, response_model=ProductModel)
async def create_new_product(product: ProductModel):
    try:
        LOGGER.info(f'Starting create new product: {product.descricao}')
        response = await ProductService().create_new_product(product=product, db=get_session)
        return JSONResponse(content=response, status_code=HTTPStatus.CREATED)
    except FieldWithValueLessThanZero as exc:
        return JSONResponse(content={"message": FIELD_VALUE_LESS_THAN_ZERO}, status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    except ProductAlreadyRegistered as exc:
        return JSONResponse(content={"message": PRODUCT_ALREADY_REGISTERED}, status_code=HTTPStatus.CONFLICT)
    except HTTPException as http_exc:
        LOGGER.error(traceback.format_exc())
        return JSONResponse(content={"message": http_exc.detail}, status_code=http_exc.status_code)
    except ServerException as exc:
        LOGGER.error(traceback.format_exc())
        return JSONResponse(content={"message": exc.message}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    except Exception as exc:
        LOGGER.error(traceback.format_exc())
        LOGGER.info(f'Exception: {exc}')
        return await JSONResponse(content={"message": str(exc)}, status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
