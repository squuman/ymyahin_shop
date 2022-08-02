import asyncio
from config import config
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from elements.keyboards import Keyboards

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)


class BotStates(StatesGroup):
    main_page = State()
    catalog_page = State()
    cart_page = State()


async def main_page_command_handler(message: types.Message):
    await BotStates.main_page.set()
    await message.reply(message.text, reply=False, reply_markup=Keyboards.main_menu())


async def catalog_page_command_handler(message: types.Message):
    await BotStates.catalog_page.set()
    await message.reply(message.text, reply=False, reply_markup=Keyboards.catalog_menu())


async def cart_page_command_handler(message: types.Message):
    await BotStates.cart_page.set()
    await message.reply(message.text, reply=False, reply_markup=Keyboards.cart_menu())


async def admin_page_command_handler(message: types.Message):
    await BotStates.cart_page.set()
    await message.reply(message.text, reply=False, reply_markup=Keyboards.admin_menu())


async def register_commands(dp):
    dp.register_message_handler(main_page_command_handler, commands='main_page', state='*')
    dp.register_message_handler(catalog_page_command_handler, commands='catalog_page', state='*')
    dp.register_message_handler(cart_page_command_handler, commands='cart_page', state='*')
    dp.register_message_handler(admin_page_command_handler, commands='admin_page', state='*')


async def main():
    await register_commands(dp)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
