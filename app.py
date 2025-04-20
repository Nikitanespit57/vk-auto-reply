from flask import Flask, request, Response
import datetime
import requests

app = Flask(__name__)

TOKEN = 'vk1.a.FZOgrA0xWTrDN4l5_WuToCk3GxyXDzblJapmESKH1HB4ulDucLPtute0HJBZBJsc0s7kV8fSNXRF7-WB1iw4OmYVTK27N5F1S0SJiRh1xjeyGU5ARj3jtb-3G1zTmr9zThgJWOi-izIrrZm7fWSOiO98gwmn0ZI1ohvGDSxoEqf4TCCnGhnVs_u7A-jZl6MeiMGzQCOPcke51kFP1Ihlkw'
CONFIRMATION_TOKEN = '5ca8abb0'
API_URL = 'https://api.vk.com/method/'

@app.route('/')
def index():
    return 'Бот работает!'

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
        return Response(CONFIRMATION_TOKEN, status=200, mimetype='text/plain')

    if data['type'] == 'message_new':
        user_id = data['object']['message']['from_id']
        now = datetime.datetime.now().time()
        if now >= datetime.time(19, 0) or now < datetime.time(11, 0):
            send_message(user_id, "Извините, наш магазин уже закрыт. Менеджер ответит с 11:00. Хорошего вечера!")

    return 'ok'