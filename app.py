import datetime
import requests
from flask import Flask, request

app = Flask(__name__)  # СНАЧАЛА создаём объект app

@app.route('/')
def index():
    return 'Бот работает!'

TOKEN = 'ВАШ_ТОКЕН_СООБЩЕСТВА'
CONFIRMATION_TOKEN = 'ВАШ_КОД_ПОДТВЕРЖДЕНИЯ_ОТ_VK'
API_URL = 'https://api.vk.com/method/'

def send_message(user_id, message):
    requests.post(API_URL + 'messages.send', params={
        'user_id': user_id,
        'message': message,
        'random_id': 0,
        'access_token': TOKEN,
        'v': '5.131'
    })

@app.route('/callback', methods=['POST'])
def callback():
    data = request.get_json()
    if data['type'] == 'confirmation':
        return CONFIRMATION_TOKEN

    if data['type'] == 'message_new':
        user_id = data['object']['message']['from_id']
        now = datetime.datetime.now().time()
        if now >= datetime.time(19, 0) or now < datetime.time(11, 0):
            send_message(user_id, "Извините, наш магазин уже закрыт. Менеджер ответит с 11:00. Хорошего вечера!")

    return 'ok'