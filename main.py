import logging
from logging.config import fileConfig

from fastapi import FastAPI
from core.configs import settings
from router.routers import api_router

fileConfig('config/logging_config.ini')
LOGGER = logging.getLogger('sLogger')

app = FastAPI(title='Watersys - API')
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000,
                log_level='info', reload=True, reload_excludes='./bot/*')
