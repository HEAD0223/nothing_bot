import asyncio
from aiogram import types
from aiogram import Dispatcher, types
from utils.db_api.db_quick_commands import select_user

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher.handler import CancelHandler

class ThrottlingMiddleware(BaseMiddleware):
	def __init__(self, limit: int = 5):
		BaseMiddleware.__init__(self)
		self.rate_limit = limit


	async def on_process_message(self, message: types.Message, data: dict):
		dp = Dispatcher.get_current()
		try:
			await dp.throttle(key='antiflood', rate=self.rate_limit)
		except Throttled as _t:
			await self.message_throttle(message, _t)
			raise CancelHandler()

	async def message_throttle(self, message: types.Message, throttled: Throttled):
		user = select_user(message.from_user.id)
		if user.language == "ru":
			text = "Обнаружен флуд (5 секунд перезарядка)"
		elif user.language == "ro":
			text = "Inundație detectată (răcire de 5 secunde)"
		else:
			text = "Flood detected (5 second cooldown)"

		delta = throttled.rate - throttled.delta
		if throttled.exceeded_count <= 3:
			await message.answer(text)
		await asyncio.sleep(delta)

