async def on_startup(dp):
    # await bot.set_webhook(config.WEBHOOK_URL)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

async def on_shutdown(dp):
    logging.warning('Shutting down..')
    # await bot.delete_webhook()
    logging.warning('Bye!')


if __name__ == '__main__':
    import os
    from data import config
    from aiogram import executor
    from aiogram.dispatcher.webhook import SendMessage
    from handlers import dp
    from handlers.middlewares import ThrottlingMiddleware

    dp.middleware.setup(ThrottlingMiddleware())
    # executor.start_webhook(
    #     dispatcher = dp,
    #     webhook_path=config.WEBHOOK_PATH,
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     skip_updates=True,
    #     host=config.WEBAPP_HOST,
    #     port=config.WEBAPP_PORT)
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)