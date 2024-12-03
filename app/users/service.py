from app.users.models import Users
from app.service.base import BaseService


class UserService(BaseService):
    model = Users