from base.repositories.repository import Repository
from base.models.user_model import UserModel


class UsersRepository(Repository):
    model = UserModel()
    table = "users"
