import asyncio
import json
import logging
from config import config
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from base.controllers.product_controller import ProductController
from base.controllers.order_controller import OrderController
from base.controllers.user_controller import UserController
from base.controllers.cart_controller import CartController
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

product_controller = ProductController()
order_controller = OrderController()
user_controller = UserController()
cart_controller = CartController()

telegram_user_id = -1
telegram_user_name = ""
telegram_user_nickname = ""

user_id = -1


class BotStates(StatesGroup):
    main_page = State()
    catalog_page = State()
    cart_page = State()
    admin = State()
    orders_page = State()


async def start_page_command_handler(message: types.Message):
    await user_information(message)
    user_id = user_controller.get_user_id_by_telegram_id(telegram_user_id, telegram_user_name,
                                                         telegram_user_nickname)
    if user_id == None:
        user_controller.create_user(telegram_user_id, telegram_user_name, telegram_user_nickname)
        user_id = user_controller.get_user_id_by_telegram_id(telegram_user_id, telegram_user_name,
                                                             telegram_user_nickname)


async def main_page_command_handler(message: types.Message):
    await BotStates.main_page.set()
    await user_information(message)
    keyboards = types.InlineKeyboardMarkup()
    keyboards.add(InlineKeyboardButton("Показать каталог", callback_data='show_catalog'))
    keyboards.add(InlineKeyboardButton("Открыть корзину", callback_data='show_cart'))
    keyboards.add(InlineKeyboardButton("Показать мои заказы", callback_data='show_orders'))
    user_name = telegram_user_name.replace("\'", "")
    await bot.send_message(message.chat.id, text=f'Здравствуйте, {user_name}! Выберите одно из следующих действий',
                           reply_markup=keyboards)


async def main_page_callback(call: types.CallbackQuery):
    choose = call.data.split('_')[1]
    if choose == "catalog":
        await catalog_page_command_handler(call.message)
    elif choose == "cart":
        await cart_page_command_handler(call.message)
    elif choose == "orders":
        await orders_page_command_handler(call.message)
    else:
        await call.message.answer("Ошибка!")


async def orders_page_command_handler(message: types.Message):
    await BotStates.orders_page.set()
    await user_information(message)
    global user_id
    if user_id == -1:
        user_id = user_controller.get_user_id_by_telegram_id(telegram_user_id, telegram_user_name,
                                                             telegram_user_nickname)
    try:
        await bot.send_message(message.chat.id, text="Ваши заказы:")
        orders_list = order_controller.get_user_orders(user_id)
        if len(orders_list) > 0:
            for order in orders_list:
                products = json.loads(order[2], strict=False)
                order_description = f"Заказ №{order[0]}:\n"
                for product in products:
                    order_description += f'''Продукт {product["id"][1]} стоимостью {product["id"][2]} в количестве {product["amount"]}\n'''
                order_description += f"Итоговая стоимость: {order[3]}"
                await bot.send_message(message.chat.id, text=order_description)
        else:
            await bot.send_message(message.chat.id, text="У вас нет заказов")
    except Exception as e:
        print(e)


async def catalog_page_command_handler(message: types.Message):
    await BotStates.catalog_page.set()
    await user_information(message)
    await bot.send_message(message.chat.id, text="Каталог товаров:")
    for product in product_controller.get_products_keyboards():
        await bot.send_message(message.chat.id, text=product['text'], reply_markup=product['keyboard'])


async def cart_page_command_handler(message: types.Message):
    await BotStates.cart_page.set()
    await user_information(message)
    await bot.send_message(message.chat.id, text="В вашей корзине следующие товары:")
    global user_id
    try:
        if user_id == -1:
            user_id = user_controller.get_user_id_by_telegram_id(telegram_user_id, telegram_user_name,
                                                                 telegram_user_nickname)
        if str(user_id).isnumeric():
            cart_items_list = cart_controller.get_cart_items_list(user_id)
            if cart_items_list == []:
                await bot.send_message(message.chat.id, "В вашей корзине нет товаров.")
            else:
                for product in cart_items_list:
                    product_info = f'''Название товара: {product["id"][1]}
Цена за штуку: {product["id"][2]}
Описание товара: {product["id"][3]}
Количество: {product["amount"]}
                    '''
                    keyboards = InlineKeyboardMarkup()
                    keyboards.add(
                        InlineKeyboardButton("Убрать одну штуку", callback_data=f'cart_remove_one_{product["id"][0]}'))
                    keyboards.add(
                        InlineKeyboardButton("Убрать из корзины", callback_data=f'cart_remove_all_{product["id"][0]}'))
                    await bot.send_message(message.chat.id, text=product_info, reply_markup=keyboards)
                if len(cart_items_list) > 0:
                    keyboards = InlineKeyboardMarkup()
                    keyboards.add(InlineKeyboardButton("Оформить", callback_data='order_create'))
                    await bot.send_message(message.chat.id, text="Желаете оформить заказ?", reply_markup=keyboards)
    except Exception as e:
        print(e)


async def cart_remove_callback(call: types.CallbackQuery):
    product_id = call.data.split("_")[3]
    cart = cart_controller.get_user_cart(user_id)
    cart_items_list = json.loads(cart[0][1], strict=False)
    if call.data.startswith('cart_remove_one_'):
        for product in cart_items_list:
            if str(product["id"][0]) == str(product_id):
                product["amount"] -= 1
                if product["amount"] <= 0:
                    try:
                        cart_items_list.remove(product)
                        # обновляем значения в базе данных
                        cart_controller.add_to_cart(cart_items_list, cart[0][0])
                        await call.message.delete()
                    except Exception as e:
                        print(e)
                else:
                    cart_controller.add_to_cart(cart_items_list, cart[0][0])
                    product_info = f'''Название товара: {product["id"][1]}
Цена за штуку: {product["id"][2]}
Описание товара: {product["id"][3]}
Количество: {product["amount"]}'''
                    keyboards = InlineKeyboardMarkup()
                    keyboards.add(
                        InlineKeyboardButton("Убрать одну штуку", callback_data=f'cart_remove_one_{product["id"][0]}'))
                    keyboards.add(
                        InlineKeyboardButton("Убрать из корзины", callback_data=f'cart_remove_all_{product["id"][0]}'))

                    await call.message.edit_text(product_info, reply_markup=keyboards)
                break
    elif call.data.startswith('cart_remove_all_'):
        for product in cart_items_list:
            if str(product["id"][0]) == str(product_id):
                try:
                    cart_items_list.remove(product)
                    # обновляем значения в базе данных
                    cart_controller.add_to_cart(cart_items_list, cart[0][0])
                    await call.message.delete()
                except Exception as e:
                    print(e)


async def admin_page_command_handler(message: types.Message):
    await BotStates.admin.set()
    await user_information(message)
    user = user_controller.get_user(telegram_user_id)
    if user[4] == 1:
        keyboards = InlineKeyboardMarkup()
        # Кнопки админа
        keyboards.add(InlineKeyboardButton("Заказы", callback_data='list_orders'))
        keyboards.add(InlineKeyboardButton("Пользователи", callback_data='list_users'))
        await bot.send_message(message.chat.id, text='Выберите действие', reply_markup=keyboards)
    else:
        await bot.send_message(message.chat.id, text="Данная функция доступна только администраторам")


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
    #
    global user_id
    if user_id == -1:
        user_id = user_controller.get_user_id_by_telegram_id(telegram_user_id, telegram_user_name,
                                                             telegram_user_nickname)

    if str(user_id).isnumeric():
        product_id = callback_query.data.split("add_to_cart_")
        await fill_cart(user_id, int(product_id[1]))
        await bot.answer_callback_query(callback_query_id=callback_query.id,
                                        text=f"Товар {product_id[1]} добавлен в корзину", show_alert=False)
    #


async def fill_cart(user_id, product_id):
    try:
        cart = cart_controller.get_user_cart(user_id)
        product = product_controller.get_product(product_id)
        cart_item = []
        cart_item.append({
            "id": product[0],
            'amount': 1
        })
        if cart == ():
            cart_controller.create_new_cart(values=[f"\'{str(json.dumps(cart_item))}\'", f"\'{str(user_id)}\'", '1'])
        else:
            product = list(product[0])
            cart_items_list = json.loads(cart[0][1], strict=False)
            i = 0
            while i < len(cart_items_list):
                if cart_items_list[i]["id"] == product:
                    break
                i += 1

            if i != len(cart_items_list):
                cart_items_list[i]["amount"] += 1
            else:
                cart_items_list.append({
                    "id": product,
                    'amount': 1
                })
            cart_controller.add_to_cart(cart_items_list, cart[0][0])

    except Exception as e:
        print(e)


# Получение информации о пользователе: его id, имя, ник
async def user_information(message):
    global telegram_user_id, telegram_user_nickname, telegram_user_name
    if telegram_user_id == -1:
        telegram_user_id = str(message.from_user.id)

        telegram_user_name = ""
        if message.from_user.first_name is not None:
            telegram_user_name += message.from_user.first_name
        telegram_user_name += " "
        if message.from_user.last_name is not None:
            telegram_user_name += message.from_user.last_name
        telegram_user_name = telegram_user_name.strip()
        if telegram_user_name == "":
            telegram_user_name = "\'No name\'"
        else:
            telegram_user_name = f"\'{telegram_user_name}\'"

        if message.from_user.username is None:
            telegram_user_nickname = f"\'No username\'"
        else:
            telegram_user_nickname = f"\'{message.from_user.username}\'"


async def order_create_callback(call: types.CallbackQuery):
    try:
        global user_id
        if user_id == -1:
            user_id = user_controller.get_user_id_by_telegram_id(telegram_user_id, telegram_user_name,
                                                                 telegram_user_nickname)
        cart_items_list = cart_controller.get_cart_items_list(user_id)
        sum = 0
        for product in cart_items_list:
            sum += int(product["id"][2]) * int(product["amount"])
        if len(cart_items_list) > 0:
            order_controller.create(values=[str(user_id), f"\'{json.dumps(cart_items_list)}\'", str(sum)])
            cart_controller.cart_close(user_id)
            await call.message.answer(f"Заказ оформлен. Стоимость: {sum}")
        else:
            await call.message.answer("Ошибка! Ваша корзина пуста.")
    except Exception as e:
        print(e)


async def register_handlers(dp):
    dp.register_message_handler(main_page_command_handler, commands='main_page', state='*')
    dp.register_message_handler(catalog_page_command_handler, commands='catalog_page', state='*')
    dp.register_message_handler(cart_page_command_handler, commands='cart_page', state='*')
    dp.register_message_handler(admin_page_command_handler, commands='admin', state='*')
    dp.register_message_handler(orders_page_command_handler, commands='orders_page', state='*')
    dp.register_message_handler(start_page_command_handler, commands='start', state='*')

    dp.register_callback_query_handler(add_to_cart_handler, lambda c: c.data and c.data.startswith("add_to_cart"),
                                       state=BotStates.catalog_page)
    dp.register_callback_query_handler(admin_callback_handler, lambda c: c.data and c.data.startswith("list_"),
                                       state=BotStates.admin)
    dp.register_callback_query_handler(cart_remove_callback, lambda c: c.data and c.data.startswith("cart_remove_"),
                                       state=BotStates.cart_page)
    dp.register_callback_query_handler(order_create_callback, lambda c: c.data and c.data.startswith("order_create"),
                                       state='*')
    dp.register_callback_query_handler(main_page_callback, lambda c: c.data and c.data.startswith("show_"),
                                       state=BotStates.main_page)


async def main():
    await register_handlers(dp)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
