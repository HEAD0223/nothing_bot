from aiogram import types
from loader import dp
from loader import bot

from utils.db_api.db_quick_commands import select_user
from keyboards.hub_keyboard import hub_kb

@dp.message_handler(commands=['hub'])
async def command_hub(message: types.Message):
    user = select_user(message.from_user.id)

    if user.language == "ru":
        text = "Главное Меню"
    elif user.language == "ro":
        text = "Meniu Principal"
    else:
        text = "Main Menu"

    await message.answer(text, reply_markup=hub_kb(message.from_user.id))
    await message.delete()