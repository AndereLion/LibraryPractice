from aiogram import executor

from library_bot.bot import dp


async def on_startup(dispatcher):
    print('Starting bot')


async def on_shutdown(dispatcher):
    print('Stopping bot')


if __name__ == '__main__':
    executor.start_polling(
        dp,
        skip_updates=False,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
