from base.controllers.controller import Controller
from base.repositories.cart_repository import CartRepository


class CartController(Controller):
    repository = CartRepository()
    def get_user_cart(self, user_id):
        return self.repository.get_data(additional_condition=f"where user_id like {user_id}")

    def add_to_cart(self):
        pass

    def del_from_cart(self, offer_id, cart_id):
        pass
