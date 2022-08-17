from base.models.model import Model


class CartModel(Model):
    fields = ["product_list", "user_id", "is_offered"]
