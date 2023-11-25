import logging

from sqlalchemy.ext.asyncio import AsyncSession
from models.client_model import ClientModel
from exceptions.client_exceptions import ClientAlreadyRegistered
from fastapi import Depends

from core.deps import get_session

LOGGER = logging.getLogger('sLogger')


class ClientValidation:

    @staticmethod
    def validate_cpf_is_unique(cpf: str, db: AsyncSession = Depends(get_session)):
        LOGGER.info('Verfying if tax id is already in database')
        with db as session:
            client = session.get(ClientModel, cpf)
            if client:
                raise ClientAlreadyRegistered()
