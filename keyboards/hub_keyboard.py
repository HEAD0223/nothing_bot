from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import datetime
from aiogram import types
from loader import dp
from loader import bot
from handlers.fsm import FSMAdmin
from aiogram.dispatcher import FSMContext
from keyboards.trade_keyboard import trade_kb
from keyboards.profile_keyboard import profile_kb
from keyboards.help_keyboard import help_kb
from keyboards.language_keyboard import lang_kb
from utils.db_api.db_quick_commands import select_user, check_created_at


############################################################################


def hub_kb(user_id):
    user = select_user(user_id)

    kb_hub = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        hub_trade   = InlineKeyboardButton("Торговать", callback_data="trade")
        hub_profile = InlineKeyboardButton("Профиль", callback_data="profile")
        hub_help    = InlineKeyboardButton("Помощь", callback_data="help")
        hub_lang    = InlineKeyboardButton("Язык", callback_data="language")
        hub_admin   = InlineKeyboardButton("Админ", callback_data="admin")
        if user.admin:
            kb_hub.add(hub_trade).add(hub_profile).row(hub_help, hub_lang).add(hub_admin)
        else:
            kb_hub.add(hub_trade).add(hub_profile).row(hub_help, hub_lang)
    elif user.language == "ro":
        hub_trade   = InlineKeyboardButton("Comerț", callback_data="trade")
        hub_profile = InlineKeyboardButton("Profil", callback_data="profile")
        hub_help    = InlineKeyboardButton("Ajutor", callback_data="help")
        hub_lang    = InlineKeyboardButton("Limba", callback_data="language")
        hub_admin   = InlineKeyboardButton("Admin", callback_data="admin")
        if user.admin:
            kb_hub.add(hub_trade).add(hub_profile).row(hub_help, hub_lang).add(hub_admin)
        else:
            kb_hub.add(hub_trade).add(hub_profile).row(hub_help, hub_lang)
    else:
        hub_trade   = InlineKeyboardButton("Trade", callback_data="trade")
        hub_profile = InlineKeyboardButton("Profile", callback_data="profile")
        hub_help    = InlineKeyboardButton("Help", callback_data="help")
        hub_lang    = InlineKeyboardButton("Language", callback_data="language")
        hub_admin   = InlineKeyboardButton("Admin", callback_data="admin")
        if user.admin:
            kb_hub.add(hub_trade).add(hub_profile).row(hub_help, hub_lang).add(hub_admin)
        else:
            kb_hub.add(hub_trade).add(hub_profile).row(hub_help, hub_lang)
    return kb_hub


############################################################################
############################################################################
############################################################################


@dp.callback_query_handler(lambda c: c.data == "trade" or c.data == "exit_trade")
async def callback_profile(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
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

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text, reply_markup=trade_kb(callback_query.from_user.id))


############################################################################


@dp.callback_query_handler(lambda c: c.data == "profile" or c.data == "exit_profile")
async def callback_profile(callback_query: types.CallbackQuery):
    user = select_user(callback_query.from_user.id)

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

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text, reply_markup=profile_kb(callback_query.from_user.id))


############################################################################


@dp.callback_query_handler(lambda c: c.data == "help")
async def callback_help(callback_query: types.CallbackQuery):
    user = select_user(callback_query.from_user.id)

    if user.language == "ru":
        text = (f"<b>О боте</b>\n"
                f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce ut.")
    elif user.language == "ro":
        text = (f"<b>Despre bot</b>\n"
                f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce ut.")
    else:
        text = (f"<b>About the bot</b>\n"
                f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce ut.")

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text, reply_markup=help_kb(callback_query.from_user.id))


############################################################################


@dp.callback_query_handler(lambda c: c.data == "language")
async def callback_hub_language(callback_query: types.CallbackQuery):
    user = select_user(callback_query.from_user.id)

    if user.language == "ru":
        text = "Пожалуйста, выберите предпочитаемый язык:"
    elif user.language == "ro":
        text = "Vă rugăm să alegeți limba preferată:"
    else:
        text = "Please choose your preferred language:"

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text, reply_markup=lang_kb(callback_query.from_user.id))


############################################################################


@dp.callback_query_handler(lambda c: c.data == "exit")
async def callback_exit(callback_query: types.CallbackQuery):
    user = select_user(callback_query.from_user.id)

    if user.language == "ru":
        text = "Главное Меню"
    elif user.language == "ro":
        text = "Meniu Principal"
    else:
        text = "Main Menu"

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text, reply_markup=hub_kb(callback_query.from_user.id))
