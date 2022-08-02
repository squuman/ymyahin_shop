from config import config
from aiogram import Bot, Dispatcher, executor, types


def main():
    bot = Bot(config.TOKEN)
    dp = Dispatcher(bot)

