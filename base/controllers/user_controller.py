from base.controllers.controller import Controller
from base.repositories.users_repository import UsersRepository


class UserController(Controller):
    repository = UsersRepository()
