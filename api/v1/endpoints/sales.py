import logging
import traceback
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from core.deps import get_session
from models.sales_model import SaleModel
from models.client_model import ClientModel
from schemas.sale_schema import SaleCreate, Sale

router = APIRouter()
LOGGER = logging.getLogger('sLogger')


@router.post('/sales', status_code=HTTPStatus.CREATED, response_model=Sale)
async def create_sale(sale: SaleCreate, db: AsyncSession = Depends(get_session)):
    LOGGER.info(f'Starting creation of a new sale: {sale}')
    try:
        async with db as session:
            client_query = select(ClientModel).where(ClientModel.cpf == sale.cpf)
            client = await session.execute(client_query)
            found_client = client.scalars().first()

            if not found_client:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Client not found')

            new_sale = SaleModel(**sale.model_dump(), client_id=found_client.id)

            LOGGER.info('Registering sale in the database')
            session.add(new_sale)
            await session.commit()
            LOGGER.info('Sale registered successfully')
            return new_sale
    except IntegrityError as exc:
        LOGGER.error(traceback.format_exc())
        LOGGER.error(f'Integrity error creating sale: {exc}')
        raise HTTPException(status_code=HTTPStatus.NOT_ACCEPTABLE,
                            detail='Integrity error creating sale')
    except Exception as exc:
        LOGGER.error(traceback.format_exc())
        LOGGER.error(f'Internal error creating sale: {exc}', exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail='Internal error processing request')
    

@router.get('/sales', response_model=list[Sale])
async def get_sales(db: AsyncSession = Depends(get_session)):
    LOGGER.info('Getting all sales')
    async with db as session:
        query = select(SaleModel)
        result = await session.execute(query)
        sales = result.scalars().unique().all()
        LOGGER.info('Retrieved all sales')
        return sales


@router.get('/sales/{sale_id}', response_model=Sale)
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


@router.delete('/sales/{sale_id}', response_model=Sale)
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