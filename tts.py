import requests
import logging
import os
from config import IAM_TOKEN, FOLDER_ID

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

save_path = 'results'
if not os.path.exists(save_path):
    os.makedirs(save_path, exist_ok=True)

def text_to_speech(text: str, voice: str, chat_id: str) -> (bool, bytes):
    headers = {
        "Authorization": f"Bearer {IAM_TOKEN}"}
    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': voice,
        'folderId': FOLDER_ID
    }
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'

    response = requests.post(url=url, data=data, headers=headers)
    if response.status_code == 200:
        file_path = os.path.join(save_path, f"{chat_id}.ogg")
        with open(file_path, "wb") as audio_file:
            audio_file.write(response.content)
        logger.info(f"Аудиофайл успешно сохранен как {file_path}")
        return True, file_path
    else:
        logger.error("При запросе в SpeechKit возникла ошибка")
        return False, "При запросе в SpeechKit возникла ошибка"