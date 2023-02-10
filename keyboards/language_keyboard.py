from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram import types
from loader import dp
from loader import bot
from utils.db_api.db_quick_commands import select_user, change_language


############################################################################


def lang_kb(user_id):
    user = select_user(user_id)

    keyboard = InlineKeyboardMarkup(resize_keyboard=True)


    if user.language == "ru":
        en_button   = InlineKeyboardButton("Английский", callback_data="en")
        ru_button   = InlineKeyboardButton("Русский", callback_data="ru")
        ro_button   = InlineKeyboardButton("Румынский", callback_data="ro")
        exit_button = InlineKeyboardButton("Выход", callback_data="exit")
        keyboard.row(ru_button, ro_button).add(en_button).add(exit_button)
    elif user.language == "ro":
        en_button   = InlineKeyboardButton("Engleză", callback_data="en")
        ru_button   = InlineKeyboardButton("Rusă", callback_data="ru")
        ro_button   = InlineKeyboardButton("Română", callback_data="ro")
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit")
        keyboard.row(ru_button, ro_button).add(en_button).add(exit_button)
    else:
        en_button   = InlineKeyboardButton("English", callback_data="en")
        ru_button   = InlineKeyboardButton("Russian", callback_data="ru")
        ro_button   = InlineKeyboardButton("Romanian", callback_data="ro")
        exit_button = InlineKeyboardButton("Exit", callback_data="exit")
        keyboard.row(ru_button, ro_button).add(en_button).add(exit_button)
    return keyboard


############################################################################
############################################################################
############################################################################


@dp.callback_query_handler(lambda c: c.data in ["en", "ru", "ro"])
async def callback_language(callback_query: types.CallbackQuery):
    language = callback_query.data
    user_id  = callback_query.from_user.id

    change_language(user_id, language)

    await bot.answer_callback_query(callback_query.id)
    if language == 'ru':
        text = 'Пожалуйста, выберите предпочитаемый язык:'
    elif language == 'ro':
        text = 'Vă rugăm să alegeți limba preferată:'
    else:
        text = 'Please choose your preferred language:'

    try:
        await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, text=text)
        await callback_query.message.edit_reply_markup(reply_markup=lang_kb(callback_query.from_user.id))
    except Exception as err:
        pass
