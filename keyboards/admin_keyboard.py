from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import paypalrestsdk
from aiogram import types
from loader import dp
from loader import bot
from handlers.fsm import FSMAdmin
from aiogram.dispatcher import FSMContext
from keyboards.hub_keyboard import hub_kb
from utils.db_api.db_quick_commands import select_user, change_support, change_sp_ticket, change_request, change_withdrawal, change_currency
from utils.db_api.db_quick_commands import get_user_sp_list, get_user_rq_list


############################################################################


def admin_kb(user_id):
    user = select_user(user_id)

    admin_kb = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        wd_button   = InlineKeyboardButton("Вывести", callback_data="admin_withdraw")
        supp_button = InlineKeyboardButton("Поддержка", callback_data="admin_support")
        exit_button = InlineKeyboardButton("Выход", callback_data="exit_admin")
        admin_kb.add(wd_button).add(supp_button).add(exit_button)
    elif user.language == "ro":
        wd_button   = InlineKeyboardButton("Retrage", callback_data="admin_withdraw")
        supp_button = InlineKeyboardButton("Suport", callback_data="admin_support")
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit_admin")
        admin_kb.add(wd_button).add(supp_button).add(exit_button)
    else:
        wd_button   = InlineKeyboardButton("Withdraw", callback_data="admin_withdraw")
        supp_button = InlineKeyboardButton("Support", callback_data="admin_support")
        exit_button = InlineKeyboardButton("Exit", callback_data="exit_admin")
        admin_kb.add(wd_button).add(supp_button).add(exit_button)
    return admin_kb


############################################################################


def admin_wd_kb(user_id):
    user = select_user(user_id)

    admin_wd_kb = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        done_button = InlineKeyboardButton("Выполнено", callback_data="admin_done")
        exit_button = InlineKeyboardButton("Выход", callback_data="exit_to_admin")
        admin_wd_kb.add(done_button).add(exit_button)
    elif user.language == "ro":
        done_button = InlineKeyboardButton("Terminat", callback_data="admin_done")
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit_to_admin")
        admin_wd_kb.add(done_button).add(exit_button)
    else:
        done_button = InlineKeyboardButton("Done", callback_data="admin_done")
        exit_button = InlineKeyboardButton("Exit", callback_data="exit_to_admin")
        admin_wd_kb.add(done_button).add(exit_button)
    return admin_wd_kb

############################################################################

def exit_rq_done_kb(user_id):
    user = select_user(user_id)

    exit_rq_done_kb = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        exit_button = InlineKeyboardButton("Выход", callback_data="exit_to_withdraw")
        exit_rq_done_kb.add(exit_button)
    elif user.language == "ro":
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit_to_withdraw")
        exit_rq_done_kb.add(exit_button)
    else:
        exit_button = InlineKeyboardButton("Exit", callback_data="exit_to_withdraw")
        exit_rq_done_kb.add(exit_button)
    return exit_rq_done_kb


############################################################################


def exit_sp_done_kb(user_id):
    user = select_user(user_id)

    exit_sp_done_kb = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        exit_button = InlineKeyboardButton("Выход", callback_data="exit_to_support")
        exit_sp_done_kb.add(exit_button)
    elif user.language == "ro":
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit_to_support")
        exit_sp_done_kb.add(exit_button)
    else:
        exit_button = InlineKeyboardButton("Exit", callback_data="exit_to_support")
        exit_sp_done_kb.add(exit_button)
    return exit_sp_done_kb


############################################################################


def exit_to_admin_kb(user_id):
    user = select_user(user_id)

    exit_to_admin_kb = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        exit_button = InlineKeyboardButton("Выход", callback_data="exit_to_admin")
        exit_to_admin_kb.add(exit_button)
    elif user.language == "ro":
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit_to_admin")
        exit_to_admin_kb.add(exit_button)
    else:
        exit_button = InlineKeyboardButton("Exit", callback_data="exit_to_admin")
        exit_to_admin_kb.add(exit_button)
    return exit_to_admin_kb


############################################################################


def exit_admin_kb(user_id):
    user = select_user(user_id)

    exit_admin_kb = InlineKeyboardMarkup(resize_keyboard=True)

    if user.language == "ru":
        exit_button = InlineKeyboardButton("Выход", callback_data="exit_admin")
        exit_admin_kb.add(exit_button)
    elif user.language == "ro":
        exit_button = InlineKeyboardButton("Ieșire", callback_data="exit_admin")
        exit_admin_kb.add(exit_button)
    else:
        exit_button = InlineKeyboardButton("Exit", callback_data="exit_admin")
        exit_admin_kb.add(exit_button)
    return exit_admin_kb


############################################################################
############################################################################
############################################################################


@dp.callback_query_handler(lambda c: c.data == "admin" or c.data == "exit_to_admin", state="*")
async def callback_help(callback_query: types.CallbackQuery):
    user = select_user(callback_query.from_user.id)

    if user.language == "ru":
        accept_text  = "Меню администратора"
        decline_text = "Вы не являетесь администратором"
    elif user.language == "ro":
        accept_text  = "Meniu administrator"
        decline_text = "Nu sunteți administrator"
    else:
        accept_text  = "Admin menu"
        decline_text = "You are not an admin"

    if user.admin:
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, accept_text, reply_markup=admin_kb(callback_query.from_user.id))
        await FSMAdmin.enter.set()
    else:
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, decline_text, reply_markup=exit_admin_kb(callback_query.from_user.id))


############################################################################


@dp.callback_query_handler(lambda c: c.data == "admin_withdraw" or c.data == "exit_to_withdraw", state=FSMAdmin.enter)
async def callback_support(callback_query: types.CallbackQuery, state: FSMContext):
    user = select_user(callback_query.from_user.id)

    user_rq = get_user_rq_list()

    if user.language == "ru":
        withdraw      = "Требуется вывод: \n"
        if user_rq:
            withdraw += (f"Пользователь  -  @{user_rq.username} ({user_rq.id})\n"
                         f"Сумма вывода  -  {user_rq.withdrawal} MDL\n"
                         f"Информация о выводе: \n"
                         f"{user_rq.card_fl}\n"
                         f"{user_rq.card_number}\n"
                         f"{user_rq.card_month}/{user_rq.card_year}  {user_rq.card_cvv2}")
        else:
            withdraw += "Нет доступных пользователей"
        no_withdraw = "В настоящее время выводы средств не требуются"
    elif user.language == "ro":
        withdraw      = "Retragere necesară:: \n"
        if user_rq:
            withdraw += (f"Utilizator  -  @{user_rq.username} ({user_rq.id})\n"
                         f"Suma de retragere  -  {user_rq.withdrawal} MDL\n"
                         f"Informații despre retragere: \n"
                         f"{user_rq.card_fl}\n"
                         f"{user_rq.card_number}\n"
                         f"{user_rq.card_month}/{user_rq.card_year}  {user_rq.card_cvv2}")
        else:
            withdraw += "Nu există utilizatori disponibile"
        no_withdraw = "În acest moment, nu sunt necesare retrageri"
    else:
        withdraw      = "Withdrawal required:: \n"
        if user_rq:
            withdraw += (f"User  -  @{user_rq.username} ({user_rq.id})\n"
                         f"Withdrawal amount  -  {user_rq.withdrawal} MDL\n"
                         f"Withdrawal information: \n"
                         f"{user_rq.card_fl}\n"
                         f"{user_rq.card_number}\n"
                         f"{user_rq.card_month}/{user_rq.card_year}  {user_rq.card_cvv2}")
        else:
            withdraw += "No users available"
        no_withdraw = "No withdrawals required at this time"

    if user_rq:
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, withdraw, reply_markup=admin_wd_kb(callback_query.from_user.id))
        await FSMAdmin.withdrawal.set()
        async with state.proxy() as data:
                data['withdrawal'] = user_rq
    else:
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, no_withdraw, reply_markup=exit_to_admin_kb(callback_query.from_user.id))


############################################################################


@dp.callback_query_handler(lambda c: c.data == "admin_support" or c.data == "exit_to_support", state=FSMAdmin.enter)
async def callback_support(callback_query: types.CallbackQuery, state: FSMContext):
    user = select_user(callback_query.from_user.id)

    user_sp = get_user_sp_list()

    if user.language == "ru":
        support      = "Требуется поддержка: \n"
        if user_sp:
            support += f"Пользователь  -  @{user_sp.username} ({user_sp.id})"
        else:
            support += "Нет доступных пользователей"
        no_support = "В настоящее время поддержка не требуется"
    elif user.language == "ro":
        support      = "Suport necesar: \n"
        if user_sp:
            support += f"Utilizator  -  @{user_sp.username} ({user_sp.id})"
        else:
            support += "Nu există utilizatori disponibile"
        no_support = "În acest moment, nu este nevoie de suport"
    else:
        support      = "Support required: \n"
        if user_sp:
            support += f"User  -  @{user_sp.username} ({user_sp.id})"
        else:
            support += "No users available"
        no_support = "No support required at this time"

    if user_sp:
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, support, reply_markup=admin_wd_kb(callback_query.from_user.id))
        await FSMAdmin.support.set()
        async with state.proxy() as data:
                data['support'] = user_sp
    else:
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, no_support, reply_markup=exit_to_admin_kb(callback_query.from_user.id))


############################################################################
############################################################################
############################################################################


@dp.callback_query_handler(lambda c: c.data == "admin_done", state=FSMAdmin.withdrawal)
async def callback_support(callback_query: types.CallbackQuery, state: FSMContext):
    user = select_user(callback_query.from_user.id)

    rq_state = await state.get_data()
    user_rq = rq_state['withdrawal']

    if user.language == "ru":
        text    = f"Вывод средств для пользователя @{user_rq.username} выполнен"
    elif user.language == "ro":
        text    = f"Retragere finalizată pentru utilizatorul @{user_rq.username}"
    else:
        text    = f"Withdrawal completed for user @{user_rq.username}"

    # # Set up the PayPal API credentials
    # paypalrestsdk.configure({
    #   "mode": "sandbox", # Change to "live" when ready to go live
    #   "client_id": "Af86oh67wBWBu03Q08NNfFV6r3lsueBzbgY1wULiyvpjSRGEsghJoBj5DukFV2B-gZNG_HZAPQbdObxJ",
    #   "client_secret": "EDH1mD0KS8ws_LzlmKbpwpjzkvk8K-iFy6rcgss04ODaHGCB_zxwd-NqU__p0ThOFs6g3LkiU5Q9mO2J"
    # })

    # # Set up the payment details
    # payment = paypalrestsdk.Payment({
    #     "intent": "sale",
    #     "payer": {
    #         "payment_method": "credit_card",
    #         "funding_instruments": [{
    #             "credit_card": {
    #                 "number": "4032031099870486",
    #                 "type": "VISA",
    #                 "expire_month": "03",
    #                 "expire_year": "2028",
    #                 "cvv2": "123",
    #                 "first_name": "John",
    #                 "last_name": "Doe",
    #             }
    #         }]
    #     },
    #     "transactions": [{
    #         "amount": {
    #             "total": "100",
    #             "currency": "USD",
    #         },
    #         "description": "This is the payment transaction description12345."
    #     }]
    # })

    # # Make the payment
    # if payment.create():
    #     print("Payment to user's credit card successful.")
    #     change_request(user_rq.id, False)
    #     currency = user_rq.currency - user_rq.withdrawal
    #     change_currency(user_rq.id, currency)
    #     change_withdrawal(user_rq.id, 0)
    #     await FSMAdmin.enter.set()
    #     await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    #     await bot.send_message(callback_query.from_user.id, text, reply_markup=exit_rq_done_kb(callback_query.from_user.id))
    # else:
    #     print("Payment failed")
    #     print(payment.error)


    change_request(user_rq.id, False)
    currency = user_rq.currency - user_rq.withdrawal
    change_currency(user_rq.id, currency)
    change_withdrawal(user_rq.id, 0)
    await FSMAdmin.enter.set()

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text, reply_markup=exit_rq_done_kb(callback_query.from_user.id))


############################################################################


@dp.callback_query_handler(lambda c: c.data == "admin_done", state=FSMAdmin.support)
async def callback_support(callback_query: types.CallbackQuery, state: FSMContext):
    user = select_user(callback_query.from_user.id)

    sp_state = await state.get_data()
    user_sp = sp_state['support']

    if user.language == "ru":
        text    = f"Поддержка для пользователя @{user_sp.username} выполнена"
    elif user.language == "ro":
        text    = f"Asistența pentru utilizatorul @{user_sp.username} este finalizată"
    else:
        text    = f"Support for user @{user_sp.username} is done"

    change_support(user_sp.id, False)
    change_sp_ticket(user_sp.id)
    await FSMAdmin.enter.set()

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text, reply_markup=exit_sp_done_kb(callback_query.from_user.id))


############################################################################
############################################################################
############################################################################


@dp.callback_query_handler(lambda c: c.data == "exit_admin", state="*")
async def callback_exit(callback_query: types.CallbackQuery, state: FSMContext):
    user = select_user(callback_query.from_user.id)

    if user.language == "ru":
        text = "Главное Меню"
    elif user.language == "ro":
        text = "Meniu Principal"
    else:
        text = "Main Menu"

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text, reply_markup=hub_kb(callback_query.from_user.id))

    await state.finish()