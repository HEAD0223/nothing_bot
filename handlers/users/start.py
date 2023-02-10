import re
import datetime
from aiogram import types
from loader import dp

from aiogram.dispatcher import FSMContext
from utils.db_api.db_quick_commands import register_user, select_user, amount_buy_referral, list_amount_users
from utils.db_api.db_quick_commands import change_referral_id, change_created_at, change_amount, change_buy_amount, change_payment_id
from keyboards import reg_kb, auth_kb
from keyboards.trade_keyboard import exit_buy_sell_kb



@dp.message_handler(commands=['start'], state="*")
async def command_start(message: types.Message, state: FSMContext):
    start_url = message.get_args().split()[-1] if message.get_args() else None
    if start_url is None:
        start_url = "None"
    match = re.match(r'(payment_success)-(buy_amount)=(.*)-(payment_id)=(.*)', start_url)
    if match:
        buy_amount = int(match.group(3))
        payment_id = str(match.group(5))
        user_id = message.from_user.id
        user = select_user(user_id)
        if payment_id == user.payment_id and buy_amount == user.buy_amount:
            if user.language == "ru":
                text  = "Покупка прошла успешно!"
            elif user.language == "ro":
                text  = "Achiziția a avut succes!"
            else:
                text  = "The purchase was successful!"

            buy_amount_db = None
            change_buy_amount(user_id, buy_amount_db)
            payment_id_db = None
            change_payment_id(user_id, payment_id_db)

            now = datetime.datetime.utcnow()
            change_created_at(user_id, now)
            amount = user.amount + (buy_amount * 2)
            change_amount(user_id, amount)

            if user.referral_id:
                amount_buy_referral(user_id, buy_amount, user.referral_id)
            else:
                list_amount_users(user_id, buy_amount)

            await message.answer(text, reply_markup=exit_buy_sell_kb(message.from_user.id))
            await message.delete()

    else:
        await state.finish()

        referrer_id = message.get_args().split()[-1] if message.get_args() else None
        reg_user = register_user(message)
        user_id = message.from_user.id
        user = select_user(user_id)

        if user.language == "ru":
            exist    = "Вы успешно зарегистрировались!"
            n_exist  = "Вы успешно вошли!"
        elif user.language == "ro":
            exist    = "Te-ai înregistrat cu succes!"
            n_exist  = "Te-ai autentificat cu succes!"
        else:
            exist    = "You have successfully registered!"
            n_exist  = "You have successfully logged in!"

        if reg_user:
            if referrer_id:
                change_referral_id(user_id, referrer_id)
            else:
                pass
            await message.answer(exist, reply_markup=reg_kb())
        else:
            await message.answer(n_exist, reply_markup=auth_kb(message.from_user.id))

        await message.delete()
