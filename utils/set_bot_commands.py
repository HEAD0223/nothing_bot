from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Launch bot'),
            types.BotCommand('hub', 'Main menu'),
            types.BotCommand('trade', 'Trade system'),
            types.BotCommand('profile', 'View profile'),
            types.BotCommand('referral', 'Referral system'),
            types.BotCommand('language', 'Select language'),
            types.BotCommand('help', 'About the bot / Support'),
        ]
    )