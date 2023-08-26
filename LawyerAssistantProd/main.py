import os
from bot import TelegramBot
from llm.llm_service import pdf_qa_template


def laborcode_ai(request):
	if request.method == 'POST':
		chroma_db_path = "prod_chroma"
		llm_service = pdf_qa_template(chroma_db_path=chroma_db_path)
		bot = TelegramBot(bot_token=os.environ["TELEGRAM_TOKEN"],
		                  llm_service=llm_service)
		bot.run_webhook(request)
		return "OK"
	return "Invalid request method"

if __name__ == '__main__':
	os.environ["TELEGRAM_BOT_API"] = "TOKEN"
	mybot = TelegramBot(os.environ["TELEGRAM_BOT_API"])
	mybot.run_pooling()