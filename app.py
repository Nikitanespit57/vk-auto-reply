from flask import Flask, request, Response
import requests
import datetime

app = Flask(__name__)

TOKEN = 'vk1.a.2KD2dV8S5a0wHw-dfsskcIvd6_PDBzwSKyUkLk6oilxIJAt0TZQ5tJuE1K1dhbtKBLl1qpVjlQgmcsgh0r5mZYltCp4bEQUg7Y5sl4PywlbXFNjtLFfs2S7L5Ii1AkUjXjSM0U3wQBXKKe2DX_cYvKmXgDIvyauZ0fSz0hU4kqXmIahKGmOkehECIOiuydVelEsdlVz9ELoJe7JjBAePeQ'
CONFIRMATION_TOKEN = '669a4c52'
API_URL = 'https://api.vk.com/method/'

@app.route('/')
def index():
    return 'Бот работает!'

@app.route('/callback', methods=['POST'])
def callback():
    data = request.get_json()
    print("Получены данные:", data)

    if data.get('type') == 'confirmation':
        return Response(CONFIRMATION_TOKEN, content_type='text/plain')

    if data.get('type') == 'message_new':
        user_id = data['object']['message']['from_id']
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        print("Текущее время:", now.time())

        if now.time() >= datetime.time(19, 0) or now.time() < datetime.time(11, 0):
            print("Отправляем сообщение пользователю:", user_id)
            send_message(user_id, "Извините, наш магазин закрыт. Менеджер ответит с 11:00, всего вам хорошего!")

    return 'ok', 200

def send_message(user_id, message):
    response = requests.post(API_URL + 'messages.send', params={
        'user_id': user_id,
        'message': message,
        'random_id': 0,
        'access_token': TOKEN,
        'v': '5.131'
    })
    print("Ответ от VK:", response.text)
  