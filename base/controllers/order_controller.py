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


    def get_user_orders(self, user_id):
        return self.repository.get_data(additional_condition=f" WHERE user_id LIKE {user_id}")

    def create_order(self, values: list):
        return self.create(values)
