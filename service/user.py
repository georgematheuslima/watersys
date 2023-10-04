import logging
import traceback

from models.user_model import UserDataModel


LOGGER = logging.getLogger("sLogger")


class UserService:
    def create_new_user(self, user_data:UserDataModel):
        LOGGER.info(f'Creating new user')