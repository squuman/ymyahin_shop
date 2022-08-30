import asyncio
import logging
from config import config
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from base.controllers.product_controller import ProductController
from base.controllers.order_controller import OrderController
from base.controllers.user_controller import UserController
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

product_controller = ProductController()
order_controller = OrderController()
user_controller = UserController()


class BotStates(StatesGroup):
    main_page = State()
    catalog_page = State()
    cart_page = State()
    admin = State()


async def main_page_command_handler(message: types.Message):
    await BotStates.main_page.set()


async def catalog_page_command_handler(message: types.Message):
    await BotStates.catalog_page.set()

    for product in product_controller.get_products_keyboards():
        await bot.send_message(message.chat.id, text=product['text'], reply_markup=product['keyboard'])


async def cart_page_command_handler(message: types.Message):
    await BotStates.cart_page.set()


async def admin_page_command_handler(message: types.Message):
    await BotStates.admin.set()
    keyboards = InlineKeyboardMarkup()
    # Кнопки админа
    keyboards.add(InlineKeyboardButton("Заказы", callback_data='list_orders'))
    keyboards.add(InlineKeyboardButton("Пользователи", callback_data='list_users'))
    await bot.send_message(message.chat.id, text='Выберите действие', reply_markup=keyboards)


async def admin_callback_handler(call: types.CallbackQuery):
    if call.data == 'list_orders':
        for order in order_controller.get_orders_keyboards():
            await call.message.answer(text=order['text'])
    elif call.data == 'list_users':
        for user in user_controller.get_users_keyboards():
            await call.message.answer(text=user['text'])
    else:
        logging.warning("unknown callback data")


async def add_to_cart_handler(callback_query: types.CallbackQuery):
    print(callback_query.data)


async def register_handlers(dp):
    dp.register_message_handler(main_page_command_handler, commands='main_page', state='*')
    dp.register_message_handler(catalog_page_command_handler, commands='catalog_page', state='*')
    dp.register_message_handler(cart_page_command_handler, commands='cart_page', state='*')
    dp.register_message_handler(admin_page_command_handler, commands='admin', state='*')

    dp.register_callback_query_handler(add_to_cart_handler, lambda c: c.data and c.data.startswith("add_to_cart"),
                                       state=BotStates.catalog_page)
    dp.register_callback_query_handler(admin_callback_handler, lambda c: c.data and c.data.startswith("list_"),
                                       state=BotStates.admin)


async def main():
    await register_handlers(dp)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
