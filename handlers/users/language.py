from aiogram import types
from loader import dp
from loader import bot

from keyboards.language_keyboard import lang_kb
from utils.db_api.db_quick_commands import select_user


@dp.message_handler(commands=['language'])
async def command_language(message: types.Message):
    user = select_user(message.from_user.id)

    await message.delete()

    if user.language == "ru":
        text = "Пожалуйста, выберите предпочитаемый язык:"
    elif user.language == "ro":
        text = "Vă rugăm să alegeți limba preferată:"
    else:
        text = "Please choose your preferred language:"
    return await message.answer(text, reply_markup=lang_kb(message.from_user.id))
