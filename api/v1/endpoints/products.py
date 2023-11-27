import logging
import traceback
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.future import select

from models.products_model import ProductModel
from schemas.product_schema import ProductSchema, ProductSchemaReturn
from validation.product import ProductValidation
from exceptions.validations import FieldWithValueLessThanZero
from exceptions.product import ProductAlreadyRegistered
from exceptions.general_exceptions import ServerException
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
                response_data = {"message": "Product created successfully"}

                return JSONResponse(content=response_data, status_code=HTTPStatus.CREATED)
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
async def get_product_by_id(product_id: int, db: AsyncSession = Depends(get_session)):
    try:
        LOGGER.info(f'Getting product by id: {product_id}')
        
        async with db as session:
            product = await session.get(ProductModel, product_id)
            if product:
                product = jsonable_encoder(product)
                LOGGER.info(f'product json {product}')
                return JSONResponse(content=product, status_code=HTTPStatus.OK)
            else:
                return JSONResponse(content={"message": 'Product not found'}, status_code=HTTPStatus.NOT_FOUND)
    
    except Exception as exc:
        LOGGER.error(traceback.format_exc())
        return JSONResponse(content={"message": f'An error occurred {exc}'}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

@router.get('/products', response_model=List[ProductSchemaReturn])
async def get_all_products(db: AsyncSession = Depends(get_session)):
    try:
        LOGGER.info('Getting All Products in the database')
        async with db as session:
            try:
                query = select(ProductModel)
                result = await session.execute(query)
                products: List[ProductSchemaReturn] = result.scalars().all()

                if not products:
                    raise HTTPException(status_code=HTTPStatus.NO_CONTENT, detail="No products found")

                return products

            except sqlalchemy.exc.SQLAlchemyError as sql_exc:
                LOGGER.error(f"SQLAlchemy error: {sql_exc}")
                raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Database error")

    except Exception as exc:
        LOGGER.error(f"Error occurred: {exc}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="An error occurred")

@router.put('/product/{id}', status_code=HTTPStatus.OK, response_model=ProductSchema)
async def update_product(product_id: int, product_data: ProductSchema, db: AsyncSession = Depends(get_session)):
    try:
        LOGGER.info(f'Updating product with ID: {product_id}')
        
        async with db as session:
            product = await session.get(ProductModel, product_id)
            if product:
                for field, value in product_data.model_dump().items():
                    setattr(product, field, value)
                
                await session.commit()
                return JSONResponse(content={"message": 'Product updated successfully'}, status_code=HTTPStatus.OK)
            else:
                return JSONResponse(content={"message": 'Product not found'}, status_code=HTTPStatus.NOT_FOUND)
    
    except Exception as exc:
        LOGGER.error(traceback.format_exc())
        return JSONResponse(content={"message": f'An error occurred{exc}'}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@router.delete('/product/{id}', status_code=HTTPStatus.OK)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_session)):
    try:
        LOGGER.info(f'Deleting product with ID: {product_id}')
        
        async with db as session:
            product = await session.get(ProductModel, product_id)
            if product:
                await session.delete(product)
                await session.commit()
                return JSONResponse(content={"message": 'Product deleted successfully'}, status_code=HTTPStatus.OK)
            else:
                return JSONResponse(content={"message": 'Product not found'}, status_code=HTTPStatus.NOT_FOUND)
    
    except Exception as exc:
        LOGGER.error(traceback.format_exc())
        return JSONResponse(content={"message": 'An error occurred'}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
