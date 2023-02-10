from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram import types
from loader import dp
from loader import bot
from data.config import admins_id
from utils.db_api.db_quick_commands import select_user, change_support, add_sp_ticket


############################################################################


def help_kb(user_id):
    user = select_user(user_id)

    help_kb = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        supp_button = InlineKeyboardButton("Поддержка", callback_data="support")
        exit_button = InlineKeyboardButton("Выход", callback_data="exit")
        help_kb.add(supp_button).add(exit_button)
    elif user.language == "ro":
        supp_button = InlineKeyboardButton("Suport", callback_data="support")
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit")
        help_kb.add(supp_button).add(exit_button)
    else:
        supp_button = InlineKeyboardButton("Support", callback_data="support")
        exit_button = InlineKeyboardButton("Exit", callback_data="exit")
        help_kb.add(supp_button).add(exit_button)
    return help_kb


############################################################################
############################################################################
############################################################################


@dp.callback_query_handler(lambda c: c.data == "support")
async def callback_support(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user = select_user(user_id)

    customer_username = callback_query.from_user.username

    if user.language == "ru":
        support_text    = f"Требуется поддержка для пользователя: \n @{customer_username} ({user_id}) !"
        user_text       = "Запрос в службу поддержки отправлен!"
        decline_support = "Запрос в службу поддержки уже был отправлен!"
    elif user.language == "ro":
        support_text    = f"Suport necesar de la utilizator: \n @{customer_username} ({user_id}) !"
        user_text       = "Solicitare de asistență trimisă!"
        decline_support = "O cerere de asistență a fost deja trimisă!"
    else:
        support_text    = f"Support needed from user: \n @{customer_username} ({user_id}) !"
        user_text       = "Support request sent!"
        decline_support = "A support request has already been sent!"

    if not user.support:
        change_support(user_id, True)
        add_sp_ticket(user_id)

        for admin in admins_id:
            try:
                await bot.send_message(admin, support_text)
            except Exception as err:
                logging.exception(err)
                
        await bot.answer_callback_query(callback_query.id, user_text)
    else:
        await bot.answer_callback_query(callback_query.id, decline_support)