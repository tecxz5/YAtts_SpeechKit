import telebot
from telebot import types
import logging
from config import TOKEN
from tts import text_to_speech
from database import Database

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)
voice_choice_states = {}
chosen_voices = {}

db = Database()
db.create_database()

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
    db.add_user(chat_id)
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
        db.save_voice_choice(chat_id, call.data)
        chosen_voices[chat_id] = {call.data}
        try:
            if call.data == 'alena':
                bot.send_audio(chat_id, open('voices/alena.ogg', 'rb'))
            elif call.data == 'filipp':
                bot.send_audio(chat_id, open('voices/filipp.ogg', 'rb'))
        except Exception as e:
            bot.send_message(chat_id, f"Ошибка при отправке аудиофайла: {str(e)}\nЕсли у вам есть Telegram Premium, включите отправку голосовых сообщений")
        return

@bot.message_handler(commands=['tts'])
def tts(message):
    chat_id = message.chat.id
    chosen_voice = db.get_chosen_voice(chat_id)
    if chosen_voice:
        bot.send_message(chat_id, f"Выбран голос: {chosen_voice}.")
    else:
        bot.send_message(chat_id, "Сначала выберите голос с помощью /choose_voice.")
        return
        # Получение текущего количества символов из базы данных
    current_characters = db.get_token_count(chat_id)

        # Проверка, достаточно ли символов для обработки запроса
    if current_characters < 10:
        bot.send_message(chat_id, "Недостаточно символов. Озвучить текст невозможно")
        return

    bot.send_message(chat_id, "Пожалуйста, введите текст для синтеза речи:")
    bot.register_next_step_handler(message, handle_text)

@bot.message_handler(commands=["symbols"])
def symbols(message):
    chat_id = message.chat.id
    symbols = db.get_token_count(chat_id)
    bot.send_message(chat_id, f"Кол-во оставшихся у вас символов: {symbols}")

def handle_text(message):
    chat_id = message.chat.id
    text = message.text
    db.save_request(chat_id, text)
    current_characters = db.get_token_count(chat_id)
    if current_characters - len(text) < 0: # проверка на то, что пользователь не уйдет в минус
        bot.send_message(chat_id, "Ты перешел лимит своих токенов, сделай текст покороче")
        return
    if len(text) >= 100: # проверка на кол-во символов
        bot.send_message(chat_id, "Ты написал текст длинне 100 символов, сделай текст покороче")
        return
    voice = db.get_chosen_voice(chat_id)
    current_characters = db.get_token_count(chat_id)
    success, audio_file_path = text_to_speech(text, voice, str(chat_id))
    if success:
        db.update_token_count(chat_id, current_characters - len(text))
        bot.send_audio(chat_id, open(audio_file_path, 'rb'))
    else:
        bot.send_message(chat_id, "Ошибка при синтезе речи.")

bot.polling()