from base.controllers.controller import Controller
from base.repositories.orders_repository import OrdersRepository


class UserController(Controller):
    repository = OrdersRepository()
