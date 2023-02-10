from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import datetime
import uuid
import time
import random
from aiogram import types
from loader import dp
from loader import bot
from handlers.fsm import FSMBuy, FSMSell
from aiogram.dispatcher import FSMContext
from utils.db_api.db_quick_commands import select_user, amount_buy_referral, list_amount_users
from utils.db_api.db_quick_commands import change_created_at, check_created_at, change_amount, change_payment_id, change_buy_amount, change_withdrawal, change_currency


############################################################################


def trade_kb(user_id):
    user = select_user(user_id)

    trade_kb = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        buy_button  = InlineKeyboardButton("Купить", callback_data="buy")
        sell_button = InlineKeyboardButton("Продать", callback_data="sell")
        exit_button = InlineKeyboardButton("Выход", callback_data="exit")
        trade_kb.row(buy_button, sell_button).add(exit_button)
    elif user.language == "ro":
        buy_button  = InlineKeyboardButton("Cumpără", callback_data="buy")
        sell_button = InlineKeyboardButton("Vinde", callback_data="sell")
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit")
        trade_kb.row(buy_button, sell_button).add(exit_button)
    else:
        buy_button  = InlineKeyboardButton("Buy", callback_data="buy")
        sell_button = InlineKeyboardButton("Sell", callback_data="sell")
        exit_button = InlineKeyboardButton("Exit", callback_data="exit")
        trade_kb.row(buy_button, sell_button).add(exit_button)
    return trade_kb


############################################################################


def payment_kb(user_id, price, amount, bot_username, payment_id):
    user = select_user(user_id)

    payment_kb = InlineKeyboardMarkup(resize_keyboard=True)

    paypal_url = f"https://head0223.github.io/nothing?bot={bot_username}&payment_id={payment_id}&price={price}&amount={amount}"

    if user.language == "ru":
        pay_button  = InlineKeyboardButton("Оплатить", url=paypal_url, callback_data="payment")
        exit_button = InlineKeyboardButton("Выход", callback_data="exit_trade")
        payment_kb.add(pay_button).add(exit_button)
    elif user.language == "ro":
        pay_button  = InlineKeyboardButton("A plati", callback_data="payment")
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit_trade")
        payment_kb.add(pay_button).add(exit_button)
    else:
        pay_button  = InlineKeyboardButton("Pay", callback_data="payment")
        exit_button = InlineKeyboardButton("Exit", callback_data="exit_trade")
        payment_kb.add(pay_button).add(exit_button)
    return payment_kb


############################################################################


def sale_kb(user_id):
    user = select_user(user_id)

    sale_kb = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        sale_button  = InlineKeyboardButton("Продать", callback_data="sale")
        exit_button = InlineKeyboardButton("Выход", callback_data="exit_trade")
        sale_kb.add(sale_button).add(exit_button)
    elif user.language == "ro":
        sale_button  = InlineKeyboardButton("Vinde", callback_data="sale")
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit_trade")
        sale_kb.add(sale_button).add(exit_button)
    else:
        sale_button  = InlineKeyboardButton("Sell", callback_data="sale")
        exit_button = InlineKeyboardButton("Exit", callback_data="exit_trade")
        sale_kb.add(sale_button).add(exit_button)
    return sale_kb


############################################################################


def exit_buy_sell_kb(user_id):
    user = select_user(user_id)

    exit_buy_sell_kb = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        exit_button = InlineKeyboardButton("Выход", callback_data="exit_trade")
        exit_buy_sell_kb.add(exit_button)
    elif user.language == "ro":
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit_trade")
        exit_buy_sell_kb.add(exit_button)
    else:
        exit_button = InlineKeyboardButton("Exit", callback_data="exit_trade")
        exit_buy_sell_kb.add(exit_button)
    return exit_buy_sell_kb


############################################################################
############################################################################
############################################################################


@dp.callback_query_handler(lambda c: c.data == "buy", state=None)
async def callback_buy(callback_query: types.CallbackQuery):
    user = select_user(callback_query.from_user.id)

    if user.language == "ru":
        accept_text  = "Введите количество для покупки:"
        decline_text = "Что-то пошло не так, свяжитесь с поддержкой!"
    elif user.language == "ro":
        accept_text  = "Introduceți cantitatea de cumpărat:"
        decline_text = "A apărut o eroare, contactați asistența!"
    else:
        accept_text  = "Enter amount to buy:"
        decline_text = "Something went wrong, contact support!"


    if user.amount >= 0:
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, accept_text)
        await FSMBuy.payment.set()
    else:
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, decline_text, reply_markup=exit_buy_sell_kb(callback_query.from_user.id))


############################################################################


@dp.callback_query_handler(lambda c: c.data == "sell", state=None)
async def callback_sell(callback_query: types.CallbackQuery):
    user = select_user(callback_query.from_user.id)

    if user.language == "ru":
        accept_text  = "Введите количество на продажу:"
        decline_text = "Что-то пошло не так, свяжитесь с поддержкой!"
        none_text    = "Количество равно 0"
    elif user.language == "ro":
        accept_text  = "Introduceți cantitatea de vânzare:"
        decline_text = "A apărut o eroare, contactați asistența!"
        none_text    = "Cantitatea este 0"
    else:
        accept_text  = "Enter amount to sell:"
        decline_text = "Something went wrong, contact support!"
        none_text    = "Amount is 0"

    if user.amount >= 1:
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, accept_text)
        await FSMSell.sale.set()
    elif user.amount == 0:
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, none_text, reply_markup=exit_buy_sell_kb(callback_query.from_user.id))
    else:
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, decline_text, reply_markup=exit_buy_sell_kb(callback_query.from_user.id))


############################################################################
############################################################################
############################################################################


@dp.callback_query_handler(lambda c: c.data == "sale", state=FSMSell.amount)
async def callback_sale(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    user = select_user(user_id)

    if user.language == "ru":
        accept_text  = "Выставление на продажу прошло успешно!"
    elif user.language == "ro":
        accept_text  = "Vânzarea a fost reușită!"
    else:
        accept_text  = "The sale was successful!"

    sell_amount = await state.get_data()

    now = datetime.datetime.utcnow()
    change_created_at(user_id, now)
    amount = user.amount - sell_amount['amount']
    change_amount(user_id, amount)
    currency = sell_amount['amount'] * 20
    change_currency(user_id, currency)

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, accept_text, reply_markup=exit_buy_sell_kb(callback_query.from_user.id))


############################################################################
############################################################################
############################################################################


@dp.message_handler(state=FSMBuy.payment)
async def buy_amount(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = select_user(user_id)

    if user.language == "ru":
        accept_text      = "Ваше количество было сохранено"
        zero_text        = "Число должно быть больше 0"
        decline_text     = "Введите число!"
        wrong_text       = "Что-то пошло не так, свяжитесь с поддержкой!"
        currency_accept  = "Покупка прошла успешно!"
        currency_decline = "Вы не можете купить такое количество"
    elif user.language == "ro":
        accept_text      = "Cantitatea dvs. a fost salvată"
        zero_text        = "Numărul trebuie să fie mai mare decât 0"
        decline_text     = "Introduceți numărul!"
        wrong_text       = "A apărut o eroare, contactați asistența!"
        currency_accept  = "Achiziția a avut succes!"
        currency_decline = "Nu puteți cumpăra această cantitate"
    else:
        accept_text      = "Your amount has been saved"
        zero_text        = "The number must be greater than 0"
        decline_text     = "Enter the number!"
        wrong_text       = "Something went wrong, contact support!"
        currency_accept  = "The purchase was successful!"
        currency_decline = "You cannot buy this amount"

    me = await bot.me
    bot_username = me.username

    price = 20


    if message.text.isdigit():
        buy_amount = int(message.text)
        if buy_amount >= 1:
            if user.currency >= 20 and user.request != True:
                buy_currency = buy_amount * 20
                if buy_currency <= user.currency:
                    currency = user.currency - buy_currency
                    change_currency(user_id, currency)
                    now = datetime.datetime.utcnow()
                    change_created_at(user_id, now)
                    currency_amount = buy_currency / 20
                    amount = (currency_amount * 2) + user.amount
                    change_amount(user_id, amount)
                    await bot.send_message(message.from_user.id, currency_accept, reply_markup=exit_buy_sell_kb(message.from_user.id))
                else:
                    await bot.send_message(message.from_user.id, currency_decline, reply_markup=exit_buy_sell_kb(message.from_user.id))
            else:
                change_buy_amount(user_id, buy_amount)
                payment_id = user.payment_id
                if payment_id is None:
                    payment_id = int(time.time() * 100000) + random.randint(0, 100000)
                    change_payment_id(user_id, payment_id)
                    await message.answer(accept_text, reply_markup=payment_kb(message.from_user.id, price, buy_amount, bot_username, payment_id))
                    await FSMBuy.next()
                else:
                    await bot.send_message(message.from_user.id, wrong_text, reply_markup=exit_buy_sell_kb(message.from_user.id))
        else:
            await bot.send_message(message.from_user.id, zero_text, reply_markup=exit_buy_sell_kb(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, decline_text, reply_markup=exit_buy_sell_kb(message.from_user.id))


############################################################################


@dp.message_handler(state=FSMSell.sale)
async def sell_amount(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = select_user(user_id)

    if user.language == "ru":
        accept_text  = "Ваше количество было сохранено"
        zero_text    = "Число должно быть больше 0"
        amount_text  = "Число превосходит ваше количество"
        decline_text = "Введите число!"
    elif user.language == "ro":
        accept_text  = "Cantitatea dvs. a fost salvată"
        zero_text    = "Numărul trebuie să fie mai mare decât 0"
        amount_text  = "Numărul depăşeşte cantitatea dvs"
        decline_text = "Introduceți numărul!"
    else:
        accept_text  = "Your amount has been saved"
        zero_text    = "The number must be greater than 0"
        amount_text  = "The number exceeds your amount"
        decline_text = "Enter the number!"

    if message.text.isdigit():
        sell_amount = int(message.text)
        if sell_amount >= 1:
            if sell_amount > user.amount:
                await bot.send_message(message.from_user.id, amount_text, reply_markup=exit_buy_sell_kb(message.from_user.id))
            else:
                await message.answer(accept_text, reply_markup=sale_kb(message.from_user.id))
                async with state.proxy() as data:
                    data['amount'] = sell_amount
                await FSMSell.next()
        else:
            await bot.send_message(message.from_user.id, zero_text, reply_markup=exit_buy_sell_kb(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, decline_text, reply_markup=exit_buy_sell_kb(message.from_user.id))


############################################################################
############################################################################
############################################################################


@dp.callback_query_handler(lambda c: c.data == "exit_trade", state="*")
async def callback_trade_exit(callback_query: types.CallbackQuery, state: FSMContext):
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

    await state.finish()