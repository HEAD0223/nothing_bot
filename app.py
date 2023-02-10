async def on_startup(dp):
    await bot.set_webhook(config.URL_APP)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)
    print("Бот запущен!")

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == '__main__':
    import os
    from aiogram import executor
    from handlers import dp
    from handlers.middlewares import ThrottlingMiddleware

    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_webhook(
        dispatcher = dp,
        webhook_path='',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)))