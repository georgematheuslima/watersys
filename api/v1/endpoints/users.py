import logging
import traceback

from http import HTTPStatus
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models.user_model import UserModel
from schemas.users_schema import UserSchemaBase, UserSchemaPurchases, UserSchemaUp, UserSchemaCreate, UserSchemaBaseReturn
from core.deps import get_session, get_current_user
from core.security import generate_hast_pass
from core.auth import authenticate, create_access_token


router = APIRouter()
LOGGER = logging.getLogger('sLogger')


@router.get('/logged', response_model=UserSchemaBase)
def get_logged(logged_user: UserModel = Depends(get_current_user)):
    LOGGER.info(f'Recuperando usuário loggado')
    return logged_user


@router.post('/signup',
             status_code=status.HTTP_201_CREATED,
             response_model=UserSchemaBase)
async def post_user(user: UserSchemaCreate,
                    db: AsyncSession = Depends(get_session)):
    LOGGER.info(f'Iniciando o registro de usuário {user}')
    try:
        new_user = UserModel(name=user.name,
                             last_name=user.last_name,
                             email=user.email,
                             phone_number=user.phone_number,
                             passwd=generate_hast_pass(user.passwd),
                             is_admin=user.is_admin)

        async with db as session:
            try:
                LOGGER.info('Registrando usuário no banco de dados')
                session.add(new_user)
                await session.commit()

                LOGGER.info('Usuário registrado com sucesso')
                return new_user
            except IntegrityError as exc:
                LOGGER.error(traceback.format_exc())
                LOGGER.error(f'Erro de integridade ao criar usuário: {exc}')
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                    detail='Usuário com o mesmo email já existente')

    except Exception as exc:
        LOGGER.error(traceback.format_exc())
        LOGGER.error(f'Erro interno ao criar usuário: {exc}', exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Erro interno ao processar a requisição')


@router.get('/', response_model=List[UserSchemaBaseReturn])
async def get_users(db: AsyncSession = Depends(get_session)):
    try:
        LOGGER.info('Buscando todos os usuários')
        async with db as session:
            query = select(UserModel)
            result = await session.execute(query)
            users: List[UserSchemaBaseReturn] = result.scalars().unique().all()

            return users
    except SQLAlchemyError as db_error:
        LOGGER.error(
            f'Erro no banco de dados ao buscar usuários: {db_error}', exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail='Erro no banco de dados ao buscar usuários')
    except Exception as e:
        LOGGER.error(f'Erro em get_users: {e}', exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail='Erro interno ao processar a requisição')


@router.get('/{user_id}',
            response_model=UserSchemaPurchases,
            status_code=HTTPStatus.OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    try:
        LOGGER.info(f'Buscando usuário com ID: {user_id}')
        async with db as session:
            query = select(UserModel).filter(UserModel.id == user_id)
            result = await session.execute(query)
            user: UserSchemaPurchases = result.scalars().unique().one_or_none()

            if user:
                return user
            else:
                raise HTTPException(detail='Usuario não encontrado',
                                    status_code=HTTPStatus.NOT_FOUND)
    except SQLAlchemyError as db_error:
        LOGGER.error(
            f'Erro no banco de dados ao buscar usuário: {db_error}', exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail='Erro no banco de dados ao buscar usuário')
    except Exception as e:
        LOGGER.error(f'Erro em get_user: {e}', exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail='Erro interno ao processar a requisição')


@router.put('/{user_id}',
            response_model=UserSchemaBase,
            status_code=HTTPStatus.ACCEPTED)
async def put_user(user_id: int,
                   user: UserSchemaUp,
                   db: AsyncSession = Depends(get_session)):
    try:
        LOGGER.info(f'Atualizando usuário com ID: {user_id}')
        async with db as session:
            query = select(UserModel).filter(UserModel.id == user_id)
            result = await session.execute(query)
            user_up: UserSchemaBase = result.scalars().unique().one_or_none()

            if user_up:
                if user.name:
                    user_up.name = user.name
                if user.email:
                    user_up.email = user.email
                if user.phone_number:
                    user_up.phone_number = user.phone_number
                if user.is_admin:
                    user_up.is_admin = user.is_admin
                if user.passwd:
                    user_up.passwd = generate_hast_pass(user.passwd)

                await session.commit()

                return user_up
            else:
                raise HTTPException(detail='Usuario não encontrado',
                                    status_code=HTTPStatus.NOT_FOUND)
    except SQLAlchemyError as db_error:
        LOGGER.error(
            f'Erro no banco de dados ao atualizar usuário: {db_error}', exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail='Erro no banco de dados ao atualizar usuário')
    except Exception as e:
        LOGGER.error(f'Erro em put_user: {e}', exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail='Erro interno ao processar a requisição')


@router.delete('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    try:
        LOGGER.info(f'Deletando usuário com ID: {user_id}')
        async with db as session:
            query = select(UserModel).filter(UserModel.id == user_id)
            result = await session.execute(query)
            user_del: UserSchemaBase = result.scalars().unique().one_or_none()

            if user_del:
                await session.delete(user_del)
                await session.commit()
                return Response(status_code=HTTPStatus.NO_CONTENT)
            else:
                raise HTTPException(detail='Usuario não encontrado',
                                    status_code=HTTPStatus.NOT_FOUND)
    except SQLAlchemyError as db_error:
        LOGGER.error(
            f'Erro no banco de dados ao deletar usuário: {db_error}', exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail='Erro no banco de dados ao deletar usuário')
    except Exception as e:
        LOGGER.error(f'Erro em delete_user: {e}', exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail='Erro interno ao processar a requisição')


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_session)):
    try:
        user = await authenticate(email=form_data.username,
                                  passwd=form_data.password,
                                  db=db)
        if not user:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail='Dados de acesso incorretos')
        return JSONResponse(content={'access_token':
                                     create_access_token(sub=user.id),
                                     'token_type': 'Bearer'},
                            status_code=HTTPStatus.OK)
    except SQLAlchemyError as db_error:
        LOGGER.error(
            f'Erro no banco de dados ao fazer login: {db_error}', exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail='Erro no banco de dados ao fazer login')
    except Exception as e:
        LOGGER.error(f'Erro em login: {e}', exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail='Erro interno ao processar a requisição')
