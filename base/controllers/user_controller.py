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
        try:
            user = self.repository.get_data(additional_condition=f"WHERE telegram_id = {telegram_id}")
            if user == ():
                return None
            else:
                return user[0]
        except Exception as e:
            return e

    def create_user(self, telegram_id, telegram_name, telegram_nickname):
        return self.create(values=[telegram_name, str(telegram_id), telegram_nickname, str(0)])

    def get_user_id_by_telegram_id(self, telegram_id, telegram_name, telegram_nickname):
        try:
            user = self.repository.get_data(additional_condition=f"WHERE telegram_id = {telegram_id}")
            if user == ():
                return None
            else:
                return (user[0][0])
        except Exception as e:
            return e
