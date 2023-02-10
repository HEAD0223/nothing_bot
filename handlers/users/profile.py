from aiogram import types

from loader import dp
from utils.db_api.db_quick_commands import select_user
from keyboards.profile_keyboard import profile_kb


@dp.message_handler(commands=['profile'])
async def command_profile(message: types.Message):
    user = select_user(message.from_user.id)

    if user.language == "ru":
        text = (f"Твой профиль\n"
                f"Имя: {user.name}\n"
                f"Имя пользователя: @{user.username}\n"
                f"Количество: {user.amount}\n"
                f"MDL: {user.currency}\n"
                f"Запрос на вывод средств: {'Да' if user.request else 'Нет'}")
    elif user.language == "ro":
        text = (f"Profilul dvs\n"
                f"Nume: {user.name}\n"
                f"Nume de utilizator: @{user.username}\n"
                f"Cantitate: {user.amount}\n"
                f"MDL: {user.currency}\n"
                f"Cerere de retragere: {'Da' if user.request else 'Nu'}")
    else:
        text = (f"Your profile\n"
                f"Name: {user.name}\n"
                f"Username: @{user.username}\n"
                f"Amount: {user.amount}\n"
                f"MDL: {user.currency}\n"
                f"Withdrawal request: {'Yes' if user.request else 'No'}")

    await message.answer(text, reply_markup=profile_kb(message.from_user.id))
    await message.delete()