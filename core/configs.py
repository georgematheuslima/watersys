# from typing import List
from pydantic.v1 import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from pytz import timezone

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:123@postgres:5432/watersys'   
    DBBaseModel = declarative_base()
    TMZ = timezone('America/Sao_Paulo')
    JWT_SECRET: str = '4-xsJJiNfox6z-c5MouHK59CRHfwxE9up4vQPdyb0pY'
    ALGORITHM: str = 'HS256'
    # uma semana
    ACESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings: Settings = Settings()
