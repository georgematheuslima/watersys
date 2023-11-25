import logging
import traceback
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.future import select

from models.client_model import ClientModel
from models.address_model import AddressModel
from schemas.client_schema import ClientSchema
from exceptions.validations import FieldWithValueLessThanZero
from exceptions.client_exceptions import ClientAlreadyRegistered
from exceptions.general_exceptions import ServerException
from utils.system_messages.client.client_messages import(CLIENT_ALREADY_REGISTERED)

from core.deps import get_session

router = APIRouter()
LOGGER = logging.getLogger('sLogger')


@router.post('/client', status_code=HTTPStatus.CREATED, response_model=ClientSchema)
async def create_new_client(client: ClientSchema, db: AsyncSession = Depends(get_session)):
    try:
        LOGGER.info(f'Starting create new client: {client}')

        new_address = AddressModel(
            address=client.address.address,
            type=client.address.type,
            state=client.address.state,
            abbreviation=client.address.abbreviation,
            city=client.address.city,
            neighborhood=client.address.neighborhood,
            reference_point=client.address.reference_point
        )

        async with db as session:
            try:
                session.add(new_address)
                await session.flush()

                new_client = ClientModel(
                    client_first_name=client.client_first_name,
                    client_last_name=client.client_last_name,
                    cpf=client.tax_id,
                    address_id=new_address.id,
                    phone_number=client.phone_number,
                    email=client.email
                )

                session.add(new_client)
                await session.commit()  
                LOGGER.info('New client was created!')
                response_data = {"message": "Client created successfully"}

                return JSONResponse(content=response_data, status_code=HTTPStatus.CREATED)
            except IntegrityError as exc:
                LOGGER.error(traceback.format_exc(), exc)
                return JSONResponse(content={"message": 'An integrity error occurred'}, status_code=HTTPStatus.CONFLICT)
            except OperationalError as exc:
                LOGGER.error(traceback.format_exc(), exc)
                return JSONResponse(content={"message": 'An error occurred at DB connect'}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    except FieldWithValueLessThanZero as exc:
        return JSONResponse(content={"message": 'Field value less than zero'}, status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    except ClientAlreadyRegistered as exc:
        return JSONResponse(content={"message": 'Client already registered'}, status_code=HTTPStatus.CONFLICT)
    except HTTPException as http_exc:
        LOGGER.error(traceback.format_exc())
        return JSONResponse(content={"message": http_exc.detail}, status_code=http_exc.status_code)
    except ServerException as exc:
        LOGGER.error(traceback.format_exc())
        return JSONResponse(content={"message": exc.message}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    except Exception as exc:
        LOGGER.error(traceback.format_exc())
        return JSONResponse(content={"message": 'An error occurred'}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

@router.get('/clients', status_code=HTTPStatus.OK, response_model=List[ClientSchema])
async def get_all_clients(db: AsyncSession = Depends(get_session)):
    try:
        LOGGER.info('Getting all clients')
        
        async with db as session:
            query = select(ClientModel)
            result = await session.execute(query)
            clients = result.scalars().all()
            
            if clients:
                clients = [jsonable_encoder(client) for client in clients]
                LOGGER.info(f'All clients: {clients}')
                return JSONResponse(content=clients, status_code=HTTPStatus.OK)
            else:
                return JSONResponse(content=[], status_code=HTTPStatus.OK)
    
    except IntegrityError as exc:
        LOGGER.error('IntegrityError occurred', exc_info=True)
        return JSONResponse(content={"message": 'An integrity error occurred'}, status_code=HTTPStatus.CONFLICT)
    
    except OperationalError as exc:
        LOGGER.error('OperationalError occurred', exc_info=True)
        return JSONResponse(content={"message": 'An error occurred at DB connect'}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    
    except Exception as exc:
        LOGGER.error('An error occurred', exc_info=True)
        return JSONResponse(content={"message": f'An error occurred: {exc}'}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

@router.get('/client/{id}', status_code=HTTPStatus.OK, response_model=ClientSchema)
async def get_client_by_id(client_id: int, db: AsyncSession = Depends(get_session)):
    try:
        LOGGER.info(f'Getting client by id: {client_id}')
        
        async with db as session:
            client = await session.get(ClientModel, client_id)
            if client:
                client = jsonable_encoder(client)
                LOGGER.info(f'Client json {client}')
                return JSONResponse(content=client, status_code=HTTPStatus.OK)
            else:
                return JSONResponse(content={"message": 'Client not found'}, status_code=HTTPStatus.NOT_FOUND)
    
    except Exception as exc:
        LOGGER.error(traceback.format_exc())
        return JSONResponse(content={"message": f'An error occurred {exc}'}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

@router.put('/client/{id}', status_code=HTTPStatus.OK, response_model=ClientSchema)
async def update_client(client_id: int, client_data: ClientSchema, db: AsyncSession = Depends(get_session)):
    try:
        LOGGER.info(f'Updating client with ID: {client_id}')
        
        async with db as session:
            client = await session.get(ClientModel, client_id)
            if client:
                for field, value in client_data.model_dump().items():
                    setattr(client, field, value)
                
                await session.commit()
                return JSONResponse(content={"message": 'Client updated successfully'}, status_code=HTTPStatus.OK)
            else:
                return JSONResponse(content={"message": 'Client not found'}, status_code=HTTPStatus.NOT_FOUND)
    
    except Exception as exc:
        LOGGER.error(traceback.format_exc())
        return JSONResponse(content={"message": f'An error occurred{exc}'}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

@router.delete('/client/{id}', status_code=HTTPStatus.OK)
async def delete_client(client_id: int, db: AsyncSession = Depends(get_session)):
    try:
        LOGGER.info(f'Deleting client with ID: {client_id}')
        
        async with db as session:
            client = await session.get(ClientModel, client_id)
            if client:
                session.delete(client)
                await session.commit()
                return JSONResponse(content={"message": 'Client deleted successfully'}, status_code=HTTPStatus.OK)
            else:
                return JSONResponse(content={"message": 'Client not found'}, status_code=HTTPStatus.NOT_FOUND)
    
    except Exception as exc:
        LOGGER.error(traceback.format_exc())
        return JSONResponse(content={"message": 'An error occurred'}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
