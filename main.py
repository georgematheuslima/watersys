import logging

from logging.config import fileConfig
from fastapi import FastAPI
from routers.router import ride_router

fileConfig('config/logging_config.ini')
LOGGER = logging.getLogger('sLogger')

app = FastAPI()

app.include_router(ride_router)

