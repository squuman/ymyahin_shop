from base.repositories.repository import Repository
from base.models.order_model import OrderModel


class OrdersRepository(Repository):
    model = OrderModel()
    table = "orders"
