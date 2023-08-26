import asyncio
import logging
from storage_utils.load_from_firestore import FirestoreClient

from aiogram import Bot, Dispatcher, executor, types
logging.basicConfig(level=logging.INFO)


class TelegramBot:
	def __init__(self, bot_token, llm_service=None):
		self.admin = "alib_sa"
		self.bot = Bot(token=bot_token)
		
		self.firestore_client = FirestoreClient()
		self.allowed_users: set = self.get_allowed_users()
		self.only_allowed_users: bool = True

		self.llm_service = llm_service

		self.dp = Dispatcher(self.bot)
		self.dp.register_message_handler(self.send_welcome, commands=["start", "help"])
		self.dp.register_message_handler(self.register_user, commands=["register"])
		self.dp.register_message_handler(self.remove_user, commands=["remove"])
		self.dp.register_message_handler(self.answer_to_question)

		Bot.set_current(self.dp.bot)

	def get_allowed_users(self):
		return set(self.firestore_client.get_allowed_users())

	async def send_welcome(self, message: types.Message):
		logging.info(f"{message.from_user.username}, send_welcome")
		if self.only_allowed_users and message.from_user.username not in self.allowed_users:
			await message.answer("Привет, я юрист ассистент бот, могу отвечать на Ваши вопросы."
			                     "Пожалуйста, зарегистрируйтесь, для этого свяжитесь с админом")
		else:
			await message.answer("Привет, я юрист ассистент бот, чем могу помочь? Сейчас могу помочь Вам с Трудовым Кодексом РК."
		                     " Еще учусь, поэтому прошу прощения за возможные ошибки.")

	async def register_user(self, message: types.Message):
		logging.info(f"{message.from_user.username}, register_user")
		if message.from_user.username == self.admin:
			user_to_register = message.get_args().strip()
			if len(user_to_register) > 0:
				self.firestore_client.add_user_to_allowed(user_to_register)
				await message.answer(f"{user_to_register} registered")
			else:
				logging.info(f"Allowed users {self.allowed_users}")
				await message.answer(f"Nothing to register")
		else:
			await message.answer("Only admin can register")

	async def remove_user(self, message: types.Message):
		logging.info(f"{message.from_user.username}, remove_user")
		if message.from_user.username == self.admin:
			user_to_remove = message.get_args().strip()
			if user_to_remove == self.admin:
				logging.warning("Cannot remove admin")
				await message.answer(f"Nothing to remove")
				return
			self.firestore_client.remove_user_from_allowed(user_to_remove)
			await message.answer(f"{user_to_remove} removed")
		else:
			await message.answer("Only admin can remove")

	async def answer_to_question(self, message: types.Message):
		logging.info(f"{message.from_user.username}, text {message.text}")
		if self.only_allowed_users and message.from_user.username not in self.allowed_users:
			await message.answer("Пожалуйста, зарегистрируйтесь, для этого свяжитесь с админом")
		else:
			# do answer logic, run llm
			await message.answer("Calling AI...")
			result = self.llm_service.run(message.text)
			print(f"LLM generates {result}")
			await message.answer(result)

	def run_pooling(self):
		executor.start_polling(self.dp, skip_updates=True)

	def run_webhook(self, request):
		data = request.get_json()
		logging.info(f"Request json {data}")
		update = types.Update(**data)
		try:
			asyncio.run(self.dp.process_update(update))
		except Exception as e:
			logging.info(f"Error processing update: {e}")

		logging.info("Success")