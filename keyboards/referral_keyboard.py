from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import uuid
from aiogram import types
from loader import dp
from loader import bot
from handlers.fsm import FSMReferral
from aiogram.dispatcher import FSMContext
from utils.db_api.db_quick_commands import select_user, change_referrer_id


############################################################################


def ref_kb(user_id):
    user = select_user(user_id)

    ref_kb = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        ref_inv    = InlineKeyboardButton("Пригласить друга", callback_data="invite")
        ref_become = InlineKeyboardButton("Cтать рефералом", callback_data="become")
        ref_exit   = InlineKeyboardButton("Выход", callback_data="exit_profile")
        ref_kb.row(ref_inv,ref_become).add(ref_exit)
    elif user.language == "ro":
        ref_inv    = InlineKeyboardButton("Invita un prieten", callback_data="invite")
        ref_become = InlineKeyboardButton("Deveniți un referal", callback_data="become")
        ref_exit   = InlineKeyboardButton("Ieșire", callback_data="exit_profile")
        ref_kb.row(ref_inv,ref_become).add(ref_exit)
    else:
        ref_inv    = InlineKeyboardButton("Invite friend", callback_data="invite")
        ref_become = InlineKeyboardButton("Become referral", callback_data="become")
        ref_exit   = InlineKeyboardButton("Exit", callback_data="exit_profile")
        ref_kb.row(ref_inv,ref_become).add(ref_exit)
    return ref_kb


############################################################################


def ref_url_kb(user_id):
    user = select_user(user_id)

    ex_kb = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        exit_button = InlineKeyboardButton("Выход", callback_data="exit_referral")
        ex_kb.add(exit_button)
    elif user.language == "ro":
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit_referral")
        ex_kb.add(exit_button)
    else:
        exit_button = InlineKeyboardButton("Exit", callback_data="exit_referral")
        ex_kb.add(exit_button)
    return ex_kb


############################################################################
############################################################################
############################################################################


@dp.callback_query_handler(lambda c: c.data == "invite")
async def callback_invite(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user = select_user(user_id)

    referrer_id = user.referrer_id
    if referrer_id is None:
        referrer_id = str(uuid.uuid4())
        change_referrer_id(user_id, referrer_id)
    else:
        pass

    me = await bot.me
    bot_username = me.username
    referrer_url = f"https://t.me/{bot_username}?start={referrer_id}"

    if user.language == "ru":
        text = ("Реферальный URL-адрес: \n" + referrer_url)
    elif user.language == "ro":
        text = ("Adresa URL de recomandare: \n" + referrer_url)
    else:
        text = ("Referral URL: \n" + referrer_url)

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text, reply_markup=ref_url_kb(callback_query.from_user.id))


############################################################################


@dp.callback_query_handler(lambda c: c.data == "become", state=None)
async def callback_become(callback_query: types.CallbackQuery):
    user = select_user(callback_query.from_user.id)

    if user.language == "ru":
        referral_text    = "Вы уже являетесь рефералом!"
        no_referral_text = "Введите реферальный URL-адрес:"
    elif user.language == "ro":
        referral_text    = "Sunteți deja un referal!"
        no_referral_text = "Introduceți adresa URL de referință:"
    else:
        referral_text    = "You're already a referral!"
        no_referral_text = "Enter referral URL:"

    if user.referral_id is None:
        await FSMReferral.get_url.set()
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, no_referral_text)
    else:
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, referral_text, reply_markup=ref_url_kb(callback_query.from_user.id))


############################################################################


@dp.callback_query_handler(lambda c: c.data == "exit_referral")
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
