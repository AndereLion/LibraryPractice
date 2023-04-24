from aiogram import Bot, Dispatcher, types

from library_bot.settings import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("I don't know what to say")
