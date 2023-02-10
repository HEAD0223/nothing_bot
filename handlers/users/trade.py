import datetime
from aiogram import types
from loader import dp
from loader import bot

from utils.db_api.db_quick_commands import select_user, change_created_at, check_created_at
from keyboards.trade_keyboard import trade_kb

@dp.message_handler(commands=['trade'])
async def command_hub(message: types.Message):
    user_id = message.from_user.id
    user = select_user(user_id)

    now = datetime.datetime.utcnow()
    check_created_at(user_id, now)

    if user.language == "ru":
        text = (f"Имя пользователя: @{user.username}\n"
                f"Количество: {user.amount}")
    elif user.language == "ro":
        text = (f"Nume de utilizator: @{user.username}\n"
                f"Cantitate: {user.amount}")
    else:
        text = (f"Username: @{user.username}\n"
                f"Amount: {user.amount}")

    await message.answer(text, reply_markup=trade_kb(message.from_user.id))
    await message.delete()