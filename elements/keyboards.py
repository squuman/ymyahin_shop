from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


class Keyboards:
    @staticmethod
    def main_menu():
        keyboard = ReplyKeyboardMarkup()
        keyboard.add(KeyboardButton("Каталог"))
        keyboard.add(KeyboardButton("Корзина"))
        return keyboard

    @staticmethod
    def catalog_menu():
        return 1

    @staticmethod
    def cart_menu():
        return 1

    @staticmethod
    def admin_menu():
        return 1
