from aiogram import types
from loader import dp
from loader import bot

from urllib.parse import urlparse, parse_qs
from handlers.fsm import FSMReferral
from aiogram.dispatcher import FSMContext
from utils.db_api.db_quick_commands import select_user, change_referral_id
from keyboards.referral_keyboard import ref_kb, ref_url_kb

@dp.message_handler(commands=['referral'])
async def command_referral(message: types.Message):
    user = select_user(message.from_user.id)

    if user.language == "ru":
        text = "Рефералы"
    elif user.language == "ro":
        text = "Referiri"
    else:
        text = "Referrals"

    await message.answer(text, reply_markup=ref_kb(message.from_user.id))
    await message.delete()



@dp.message_handler(state=FSMReferral.get_url)
async def command_referral(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = select_user(user_id)

    if user.language == "ru":
        text_done  = "Вы стали рефералом!"
        text_wrong = "Неправильная ссылка."
    elif user.language == "ro":
        text_done  = "Ai devenit un referal!"
        text_wrong = "Link greșit."
    else:
        text_done  = "You have become a referral!"
        text_wrong = "Wrong link format."

    me = await bot.me
    bot_username = me.username
    ref_start = f"https://t.me/{bot_username}?start="

    if not message.text.startswith(ref_start):
        await bot.send_message(message.from_user.id, text_wrong, reply_markup=ref_url_kb(message.from_user.id))
    else:
        parsed_url = urlparse(message.text)
        query = parse_qs(parsed_url.query)
        referral_id = query.get("start", [None])[0]
        change_referral_id(user_id, referral_id)
        await message.answer(text_done, reply_markup=ref_url_kb(message.from_user.id))

    await state.finish()