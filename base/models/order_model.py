from base.models.model import Model


class OrderModel(Model):
    fields = ["user_id", "products", "sum"]
