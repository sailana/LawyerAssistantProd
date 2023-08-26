import telebot
import os
from config.config import setup_config
from llm.llm_service import pdf_qa_template

if __name__ == "__main__":
  print("Initializing ...")
  setup_config()
  bot = telebot.TeleBot(os.environ["TELEGRAM_BOT_API"])

  chroma_db_path = "chroma_db_full_kaz_adm"
  llm_service = pdf_qa_template(chroma_db_path=chroma_db_path)
  print("Initializing completed")


  @bot.message_handler(commands=['start'])
  def start_message(message):
    bot.send_message(
      message.chat.id, 'Привет, я Юрист-ассистент, чему могу помочь?')

  @bot.message_handler(content_types='text')
  def message_reply(message):
    print("--------")
    print(f"{message.chat.id} wrote {message.text}")
    print("--------")
    if message.text[0] == ".":
      input_text = message.text[1:]
      result = llm_service.run(input_text)
      bot.send_message(message.chat.id, result)
      print(f"LLM generates {result}")
    else:
      bot.send_message(
        message.chat.id, f"Вы мне написали {message.text}")


  bot.infinity_polling()
