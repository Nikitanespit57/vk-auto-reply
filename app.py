from flask import Flask, request
import requests
import datetime

app = Flask(__name__)

TOKEN = 'vk1.a.FZOgrA0xWTrDN4l5_WuToCk3GxyXDzblJapmESKH1HB4ulDucLPtute0HJBZBJsc0s7kV8fSNXRF7-WB1iw4OmYVTK27N5F1S0SJiRh1xjeyGU5ARj3jtb-3G1zTmr9zThgJWOi-izIrrZm7fWSOiO98gwmn0ZI1ohvGDSxoEqf4TCCnGhnVs_u7A-jZl6MeiMGzQCOPcke51kFP1Ihlkw'
CONFIRMATION_TOKEN = '5ca8abb0'
API_URL = 'https://api.vk.com/method/'

@app.route('/')
def index():
    return 'Бот работает!'

@app.route('/callback', methods=['POST'])
def callback():
    data = request.get_json()
    print("Получены данные:", data)

    if data.get('type') == 'confirmation':
        return CONFIRMATION_TOKEN, 200

    if data.get('type') == 'message_new':
        user_id = data['object']['message']['from_id']
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)  # Добавляем смещение на Москву
        print("Текущее время:", now.time())

        if now.time() >= datetime.time(19, 0) or now.time() < datetime.time(11, 0):
            print("Отправляем сообщение пользователю:", user_id)
            send_message(user_id, "Извините, наш магазин уже закрыт. Менеджер ответит с 11:00. Хорошего вечера!")

    return 'ok', 200

def send_message(user_id, message):
    response = requests.post(API_URL + 'messages.send', params={
        'user_id': user_id,
        'message': message,
        'random_id': 0,
        'access_token': TOKEN,
        'v': '5.131'
    })
    print("Ответ от VK при отправке сообщения:", response.text)