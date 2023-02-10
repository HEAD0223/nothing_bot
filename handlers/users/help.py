from aiogram import types
from loader import dp
from loader import bot

from utils.db_api.db_quick_commands import select_user
from keyboards.help_keyboard import help_kb

@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    user = select_user(message.from_user.id)

    if user.language == "ru":
        text = (f"<b>О боте</b>\n"
                f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce ut.")
    elif user.language == "ro":
        text = (f"<b>Despre bot</b>\n"
                f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce ut.")
    else:
        text = (f"<b>About the bot</b>\n"
                f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce ut.")

    await message.answer(text, parse_mode="HTML", reply_markup=help_kb(message.from_user.id))
    await message.delete()