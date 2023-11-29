import logging
import traceback
from datetime import datetime
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from core.deps import get_session
from models.sales_model import SaleModel
from models.client_model import ClientModel
from models.products_model import ProductModel
from schemas.sale_schema import SaleCreate, SaleAllInfo

router = APIRouter()
LOGGER = logging.getLogger('sLogger')


@router.post('/sales', status_code=HTTPStatus.CREATED)
async def create_sale(sale: SaleCreate, db: AsyncSession = Depends(get_session)):
    LOGGER.info(f'Starting creation of a new sale: {sale}')
    try:
        async with db as session:
            client_query = select(ClientModel).where(
                ClientModel.cpf == str(sale.cpf))
            client = await session.execute(client_query)
            found_client = client.scalars().first()

            if not found_client:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail='Client not found')

            product_query = select(ProductModel).where(
                ProductModel.id == sale.product_id)
            product = await session.execute(product_query)
            found_product = product.scalars().first()

            if not found_product:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail='Product not found')

            if found_product.quantidade < sale.quantity:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                    detail='Insufficient quantity in stock')

            total_amount = sale.quantity * found_product.valor_venda

            new_sale = SaleModel(
                quantity=sale.quantity,
                total_amount=total_amount,
                purchase_date=datetime.now().date(),
                returnable=sale.returnable,
                product_id=sale.product_id,
                cpf=sale.cpf
            )

            new_sale.customer = found_client

            found_product.quantidade -= sale.quantity

            LOGGER.info('Registering sale in the database')
            session.add(new_sale)
            await session.commit()
            LOGGER.info('Sale registered successfully')

            return {"Message": f"Sale registered. Sale price {total_amount}"}

    except IntegrityError as exc:
        LOGGER.error(traceback.format_exc())
        LOGGER.error(f'Integrity error creating sale: {exc}')
        raise HTTPException(status_code=HTTPStatus.NOT_ACCEPTABLE,
                            detail='Integrity error creating sale')
    except HTTPException as exc:
        LOGGER.error(f'Error creating sale: {exc.detail}')
        raise
    except Exception as exc:
        LOGGER.error(traceback.format_exc())
        LOGGER.error(f'Internal error creating sale: {exc}', exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail='Internal error processing request')


@router.get('/sales', response_model=list[SaleAllInfo])
async def get_sales(db: AsyncSession = Depends(get_session)):
    LOGGER.info('Getting all sales')
    async with db as session:
        query = select(SaleModel)
        result = await session.execute(query)
        sales = result.scalars().unique().all()
        LOGGER.info('Retrieved all sales')
        return sales

@router.get('/sales/{cpf}', response_model=List[SaleAllInfo])
async def get_sale_by_cpf(cpf: str, db: AsyncSession = Depends(get_session)):
    LOGGER.info(f'Getting sales with CPF: {cpf}')
    async with db as session:
        query = select(SaleModel).filter(SaleModel.cpf == cpf)
        result = await session.execute(query)
        sales = result.scalars().all()
        if sales:
            LOGGER.info(f'Sales with CPF {cpf} retrieved successfully')
            return [sale.__dict__ for sale in sales]
        else:
            LOGGER.warning(f'Sales with CPF {cpf} not found')
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Sales not found for the given CPF'
            )

@router.get('/sales/{sale_id}', response_model=SaleAllInfo)
async def get_sale(sale_id: int, db: AsyncSession = Depends(get_session)):
    LOGGER.info(f'Getting sale with ID: {sale_id}')
    async with db as session:
        query = select(SaleModel).filter(SaleModel.id == sale_id)
        result = await session.execute(query)
        sale = result.scalars().unique().one_or_none()
        if sale:
            LOGGER.info(f'Sale with ID {sale_id} retrieved successfully')
            return sale
        else:
            LOGGER.warning(f'Sale with ID {sale_id} not found')
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                                detail='Sale not found')


@router.get('/telegram/{client_cpf}', response_model=list[SaleAllInfo])
async def get_sale_by_cpf(client_cpf: str, db: AsyncSession = Depends(get_session)):
    LOGGER.info(f'Getting sale with ID: {client_cpf}')
    async with db as session:
        query = select(SaleModel).filter(SaleModel.cpf == client_cpf)
        print(query)
        result = await session.execute(query)
        sales = result.scalars().unique().all()
        LOGGER.info('Retrieved all sales')
        return sales


@router.delete('/sales/{sale_id}', response_model=SaleAllInfo)
async def delete_sale(sale_id: int, db: AsyncSession = Depends(get_session)):
    LOGGER.info(f'Deleting sale with ID: {sale_id}')
    async with db as session:
        query = select(SaleModel).filter(SaleModel.id == sale_id)
        result = await session.execute(query)
        sale = result.scalars().unique().one_or_none()
        if sale:
            await session.delete(sale)
            await session.commit()
            LOGGER.info(f'Sale with ID {sale_id} deleted successfully')
            return sale
        else:
            LOGGER.warning(f'Sale with ID {sale_id} not found')
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                                detail='Sale not found')
