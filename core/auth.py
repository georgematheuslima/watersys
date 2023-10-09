from pytz import timezone
from typing import Optional
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from models.user_model import UserModel
from core.configs import settings
from core.security import check_password
from pydantic import EmailStr

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_V1_STR}/users/login'
)


async def authenticate(email: EmailStr, passwd: str, db: AsyncSession) -> Optional[UserModel]:
    async with db as session:
        query = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            return None

        if not check_password(passwd, user.passwd):
            return None

        return user


def _create_token(token_type: str, lifetime: timedelta, sub: str) -> str:
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    payload = {}
    tmz = timezone('America/Sao_Paulo')
    expires = datetime.now(tz=tmz) + lifetime

    payload['type'] = token_type
    payload['exp'] = expires.timestamp()
    payload['iap'] = datetime.now(tz=settings.TMZ).timestamp()
    payload['sub'] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET,
                      algorithm=settings.ALGORITHM)


def create_access_token(sub: str) -> str:
    return _create_token(
        token_type='access_token',
        lifetime=timedelta(minutes=settings.ACESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
