import telebot
from telebot import types
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
voice_choice_states = {}

def create_voice_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    voices = ['alena', 'filipp']
    for voice in voices:
        keyboard.add(types.InlineKeyboardButton(text=voice, callback_data=voice))
    return keyboard

@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    bot.send_message(chat_id, f"""
Привет {user_name}! Это бот, который может превратить твой текст в аудиофайл(голосовое сообщение).
Чтобы начать переводить текст в аудиофайл введи /tts
Для более подробной информации по боту введи /help""")

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, """
Бот работает на базе SpeechKit V1
У пользователя нету бесконечных символов на озвучивание текста(500 на каждого пользователя)
Чтобы посмотреть оставшееся кол-во символов введите /symbols""")

@bot.message_handler(commands=['choose_voice'])
def send_key(message):
    keyboard = create_voice_keyboard()
    chat_id = message.chat.id
    bot.send_message(chat_id, "Выберите голос:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data:
        chat_id = call.message.chat.id
        bot.delete_message(chat_id, call.message.message_id)
        bot.send_message(chat_id, f"Выбран голос: {call.data}. Отправляю аудиофайл с выбранным голосом")
        voice_choice_states[chat_id] = True
        try:
            if call.data == 'alena':
                bot.send_audio(chat_id, open('voices/alena.ogg', 'rb'))
            elif call.data == 'filipp':
                bot.send_audio(chat_id, open('voices/filipp.ogg', 'rb'))
        except Exception as e:
            bot.send_message(chat_id, f"Ошибка при отправке аудиофайла: {str(e)}\nЕсли у вам есть Telegram Premium, включите отправку голосовых сообщений")
        return

@bot.message_handler(commands=["tts"])
def tts(message):
    chat_id = message.chat.id
    if chat_id in voice_choice_states and voice_choice_states[chat_id]:
        bot.send_message(chat_id, "Команда tts выполнена.")
    else:
        bot.send_message(chat_id, "Сначала выберите голос с помощью /choose_voice.")

@bot.message_handler(commands=["symbols"])
def symbols(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Команда позволяющая смотреть кол-во символов, пока заглушка")

bot.polling()