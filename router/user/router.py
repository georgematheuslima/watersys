import logging
import traceback
from http import HTTPStatus
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException

from models.user_model import UserDataModel

LOGGER = logging.getLogger('sLogger')
user_router = APIRouter(prefix='/watersys/user/v1')
user_service = UserService()

@user_router.post("/user")
async def create_user(user_data: UserDataModel):
    try:
        response = await user_service.create_new_user(user_data)