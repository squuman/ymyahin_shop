from base.models.model import Model


class UserModel(Model):
    fields = ["name", "telegram_id", "nickname", "is_admin"]
