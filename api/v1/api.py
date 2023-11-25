from fastapi import APIRouter
from api.v1.endpoints import users, purchase


api_router = APIRouter()

api_router.include_router(users.router,
                          prefix='/users',
                          tags=['Users'])
api_router.include_router(purchase.router,
                          prefix='/purchase',
                          tags=['purchase'])
