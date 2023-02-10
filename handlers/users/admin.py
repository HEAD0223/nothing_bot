from aiogram import types
from loader import dp
from loader import bot

from handlers.fsm import FSMAdmin
from aiogram.dispatcher import FSMContext
from utils.db_api.db_quick_commands import select_user
from keyboards.admin_keyboard import admin_kb, exit_admin_kb
from keyboards.hub_keyboard import hub_kb

@dp.message_handler(commands=['admin'], state=None)
async def command_admin(message: types.Message):
    user = select_user(message.from_user.id)

    if user.language == "ru":
        accept_text  = "Меню администратора"
        decline_text = "Вы не являетесь администратором"
    elif user.language == "ro":
        accept_text  = "Meniu administrator"
        decline_text = "Nu sunteți administrator"
    else:
        accept_text  = "Admin menu"
        decline_text = "You are not an admin"

    if user.admin:
        await message.answer(accept_text, reply_markup=admin_kb(message.from_user.id))
        await FSMAdmin.enter.set()
        await message.delete()
    else:
        await message.answer(decline_text, reply_markup=exit_admin_kb(message.from_user.id))
        await message.delete()