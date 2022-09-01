from base.controllers.controller import Controller
from base.repositories.cart_repository import CartRepository
import json


class CartController(Controller):
    repository = CartRepository()

    def get_cart_items_list(self, user_id):
        cart = self.get_user_cart(user_id)
        if len(cart) > 0 and cart[0][1] != '[]':
            return json.loads(cart[0][1], strict=False)
        else:
            return []

    def get_user_cart(self, user_id):
        return self.repository.get_data(additional_condition=f" WHERE user_id like {user_id} AND is_open like 1")

    def add_to_cart(self, value, cart_id):
        return self.repository.update_data("product_list", value, f"WHERE carts.id = {cart_id}")

    def create_new_cart(self, values: list):
        return self.create(values)

    def cart_close(self, user_id):
        return self.repository.update_data("is_open", 0, f"WHERE user_id LIKE {user_id} AND is_open LIKE 1")

    def del_from_cart(self, offer_id, cart_id):
        pass
