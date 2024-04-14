import requests
from config import IAM_TOKEN, FOLDER_ID

def text_to_speech(text: str) -> (bool, bytes):
    headers = {
        "Authorization": f"Bearer {IAM_TOKEN}"}
    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': "filipp",
        'folderId': FOLDER_ID
    }
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'

    response = requests.post(url=url, data=data, headers=headers)
    if response.status_code == 200:
        return True, response.content
    else:
        return False, "При запросе в SpeechKit возникла ошибка"