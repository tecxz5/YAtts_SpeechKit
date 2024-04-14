import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands="start")
def start(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    bot.send_message(chat_id, f"""
Привет {user_name}! Это бот, который может превратить твой текст в аудиофайл(голосовое сообщение).
Чтобы начать переводить текст в аудиофайл введи /tts
Для более подробной информации по боту введи /help""")

@bot.message_handler(commands="help")
def help(message):
    bot.send_message(message.chat.id, """
Бот работает на базе SpeechKit V1
У пользователя нету бесконечных символов на озвучивание текста(500 на каждого пользователя)
Чтобы посмотреть оставшееся кол-во символов введите /symbols""")

@bot.message_handler(commands="tts")
def tts(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Команда заглушка, будет зависеть от /choose_voice")

@bot.message_handler(commands="choose_voice")
def choose_voice(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Команда позволяющая выбрать голос для озвучки, недоступна")

@bot.message_handler(commands="symbols")
def symbols(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Команда позволяющая смотреть кол-во символов, пока заглушка")