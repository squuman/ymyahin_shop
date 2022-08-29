from base.controllers.controller import Controller
from base.repositories.orders_repository import OrdersRepository


class OrderController(Controller):
    repository = OrdersRepository()

    def get_orders_keyboards(self):
        orders_list = self.repository.get_data()
        orders_keyboard = []

        for order in orders_list:
            orders_keyboard.append({
                "text": f"{order[0]}\n{order[1]}\n{order[2]}"
            })
        return orders_keyboard