from base.controllers.controller import Controller
from base.repositories.users_repository import UsersRepository


class UserController(Controller):
    repository = UsersRepository()

    def get_users_keyboards(self):
        users_list = self.repository.get_data()
        users_keyboard = []

        for user in users_list:
            users_keyboard.append({
                "text": f"{user[0]}\n{user[1]}\n{user[2]}"
            })
        return users_keyboard

    def get_user(self, telegram_id):
        self.repository.get_data(additional_condition=f"WHERE telegram_id = {telegram_id}")