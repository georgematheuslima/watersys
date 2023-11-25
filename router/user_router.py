from fastapi import APIRouter
from api.v1.endpoints import users, products, client


api_router = APIRouter()

api_router.include_router(users.router, prefix='/users', tags=['Users'])
api_router.include_router(products.router, prefix='/products', tags=['Products'])
api_router.include_router(client.router, prefix='/client', tags=['client'])