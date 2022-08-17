from base.controllers.controller import Controller
from base.repositories.products_repository import ProductsRepository
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class ProductController(Controller):
    repository = ProductsRepository()

    def get_products_keyboards(self):
        products_list = self.repository.get_data()
        products_keyboard = []

        for product in products_list:
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton("Добавить в корзину", callback_data=f"add_to_cart_{product[0]}"))
            products_keyboard.append({
                "text": f"{product[1]}\n{product[3]}\n{product[2]}",
                "keyboard": keyboard
            })

        return products_keyboard
