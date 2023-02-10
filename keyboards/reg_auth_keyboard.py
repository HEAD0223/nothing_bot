from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram import types
from loader import dp
from loader import bot
from keyboards.hub_keyboard import hub_kb
from utils.db_api.db_quick_commands import select_user


############################################################################


def reg_kb():

    reg_hub  = InlineKeyboardButton('🏠', callback_data="hub")
    reg_help = InlineKeyboardButton('🆘', callback_data="help")
    reg_lang = InlineKeyboardButton('🌎', callback_data="language")

    kb_reg = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb_reg.add(reg_hub).row(reg_help, reg_lang)
    return kb_reg


############################################################################


def auth_kb(user_id):
    user = select_user(user_id)

    kb_auth = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        auth_continue = InlineKeyboardButton("Продолжить", callback_data="continue")
        kb_auth.add(auth_continue)
    elif user.language == "ro":
        auth_continue = InlineKeyboardButton("Continua", callback_data="continue")
        kb_auth.add(auth_continue)
    else:
        auth_continue = InlineKeyboardButton("Continue", callback_data="continue")
        kb_auth.add(auth_continue)
    return kb_auth


############################################################################
############################################################################
############################################################################


@dp.callback_query_handler(lambda c: c.data == "continue" or c.data == "hub")
async def callback_auth(callback_query: types.CallbackQuery):
    user = select_user(callback_query.from_user.id)

    if user.language == "ru":
        text = "Главное Меню"
    elif user.language == "ro":
        text = "Meniu Principal"
    else:
        text = "Main Menu"

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text, reply_markup=hub_kb(callback_query.from_user.id))