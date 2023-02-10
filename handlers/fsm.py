from aiogram import types
from loader import dp

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMAdmin(StatesGroup):
	enter      = State()
	support    = State()
	withdrawal = State()




class FSMCard(StatesGroup):
	number  = State()
	date    = State()
	cvv2    = State()
	fl_name = State()


class FSMReferral(StatesGroup):
	get_url = State()



class FSMBuy(StatesGroup):
	payment = State()
	amount  = State()

class FSMSell(StatesGroup):
	sale   = State()
	amount = State()