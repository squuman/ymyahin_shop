from base.repositories.repository import Repository
from base.models.cart_model import CartModel


class CartRepository(Repository):
    model = CartModel()
    table = "carts"
