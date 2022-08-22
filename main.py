import asyncio, logging
from config import config
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from base.controllers.product_controller import ProductController
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

bot = Bot("5626798897:AAFwn2YuoecFfL_qnLq5TrulgAzgyRTRGQ0")
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)
product_controller = ProductController()


class BotStates(StatesGroup) :
    main_page = State()
    catalog_page = State()
    cart_page = State()


inline_btn_catalog = InlineKeyboardButton("Каталог", callback_data="btnCatalog")
inline_btn_cart = InlineKeyboardButton("Корзина", callback_data="btnCart")
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_catalog, inline_btn_cart)

inline_btn_add = InlineKeyboardButton("+", callback_data="btnAdd")
inline_btn_remove = InlineKeyboardButton("-", callback_data="btnRemove")
inline_btn_count = InlineKeyboardButton("1", callback_data="btnCount")
inline_btn_inCart = InlineKeyboardButton("В корзину", callback_data="btnAddCart")
inline_kb2 = InlineKeyboardMarkup(row_width=3).add(inline_btn_add, inline_btn_count, inline_btn_remove,
                                                   inline_btn_inCart)



inline_btn_order = InlineKeyboardButton("Оформить заказ", callback_data="btnOrder")
inline_btn_inCartAdd = InlineKeyboardButton("+", callback_data="btnCartAdd")
inline_btn_inCartRemove = InlineKeyboardButton("-", callback_data="btnCartRemove")
inline_btn_inCartCount = InlineKeyboardButton("1", callback_data="btnCartCount")
inline_btn_inCartDel = InlineKeyboardButton("Удалить товар", callback_data="btnCartDel")
inline_btn_inCartClear = InlineKeyboardButton("Очистить корзину", callback_data="btnCartClear")
inline_kb3 = InlineKeyboardMarkup().add(inline_btn_order)
inline_kb3.row(inline_btn_inCartAdd, inline_btn_inCartCount, inline_btn_inCartRemove)
inline_kb3.add(inline_btn_inCartDel)
inline_kb3.add(inline_btn_inCartClear)


async def main_page_command_handler(message: types.Message) :
    await BotStates.main_page.set()
    await message.answer("Главное меню", reply_markup=inline_kb1)


async def catalog_page_command_handler(message: types.Message) :
    await BotStates.catalog_page.set()
    await message.answer("Каталог", reply_markup=inline_kb2)

    for product in product_controller.get_products_keyboards() :
        await bot.send_message(message.chat.id, text=product['text'], reply_markup=product['keyboard'])


# @dp.message_handler(commands="")
# async def test_commands(message : types.Message):
#     await message.answer("++", reply_markup=inline_btn_inCartAdd)
#
# @dp.callback_query_handlers(text="btnCartAdd")
# async def btnCartAdd_call(callback : types.CallbackQuery):
#     await callback.answer("test")


async def cart_page_command_handler(message: types.Message) :
    await BotStates.cart_page.set()
    await message.answer("Корзина", reply_markup=inline_kb3)


async def admin_page_command_handler(message: types.Message) :
    await BotStates.cart_page.set()
    await message.answer("Админ панель")


async def add_to_cart_handler(callback_query: types.CallbackQuery) :
    print(callback_query.data)


async def register_handlers(dp) :
    dp.register_message_handler(main_page_command_handler, commands='main_page', state='*')
    dp.register_message_handler(catalog_page_command_handler, commands='catalog_page', state='*')
    dp.register_message_handler(cart_page_command_handler, commands='cart_page', state='*')
    dp.register_message_handler(admin_page_command_handler, commands='admin_page', state='*')

    dp.register_callback_query_handler(add_to_cart_handler, lambda c : c.data and c.data.startswith("add_to_cart"),
                                       state=BotStates.catalog_page)


async def main() :
    await register_handlers(dp)
    await dp.start_polling()


if __name__ == '__main__' :
    asyncio.run(main())
