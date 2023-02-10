from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram import types
from loader import dp
from loader import bot
from keyboards.withdraw_keyboard import withdraw_kb
from keyboards.referral_keyboard import ref_kb
from utils.db_api.db_quick_commands import select_user


############################################################################


def profile_kb(user_id):
    user = select_user(user_id)

    profile_kb = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        wd_button   = InlineKeyboardButton("Вывести", callback_data="withdraw")
        ref_button  = InlineKeyboardButton("Рефералы", callback_data="referral")
        exit_button = InlineKeyboardButton("Выход", callback_data="exit")
        profile_kb.add(wd_button).add(ref_button).add(exit_button)
    elif user.language == "ro":
        wd_button   = InlineKeyboardButton("Retrage", callback_data="withdraw")
        ref_button  = InlineKeyboardButton("Referiri", callback_data="referral")
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit")
        profile_kb.add(wd_button).add(ref_button).add(exit_button)
    else:
        wd_button   = InlineKeyboardButton("Withdraw", callback_data="withdraw")
        ref_button  = InlineKeyboardButton("Referrals", callback_data="referral")
        exit_button = InlineKeyboardButton("Exit", callback_data="exit")
        profile_kb.add(wd_button).add(ref_button).add(exit_button)
    return profile_kb


############################################################################
############################################################################
############################################################################


@dp.callback_query_handler(lambda c: c.data == "referral")
async def callback_referral(callback_query: types.CallbackQuery):
    user = select_user(callback_query.from_user.id)

    if user.language == "ru":
        text = "Рефералы"
    elif user.language == "ro":
        text = "Referiri"
    else:
        text = "Referrals"

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text, reply_markup=ref_kb(callback_query.from_user.id))


############################################################################


@dp.callback_query_handler(lambda c: c.data == "withdraw" or c.data == "exit_withdraw")
async def callback_referral(callback_query: types.CallbackQuery):
    user = select_user(callback_query.from_user.id)

    if user.language == "ru":
        text = f"Вы можете вывести: {user.currency} MDL"
    elif user.language == "ro":
        text = f"Puteți retrage: {user.currency} MDL"
    else:
        text = f"You can withdraw: {user.currency} MDL"

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text, reply_markup=withdraw_kb(callback_query.from_user.id))
