from flask import Flask, request, Response
import requests
import datetime
import threading
import time

app = Flask(__name__)

TOKEN = 'vk1.a.2KD2dV8S5a0wHw-dfsskcIvd6_PDBzwSKyUkLk6oilxIJAt0TZQ5tJuE1K1dhbtKBLl1qpVjlQgmcsgh0r5mZYltCp4bEQUg7Y5sl4PywlbXFNjtLFfs2S7L5Ii1AkUjXjSM0U3wQBXKKe2DX_cYvKmXgDIvyauZ0fSz0hU4kqXmIahKGmOkehECIOiuydVelEsdlVz9ELoJe7JjBAePeQ'
CONFIRMATION_TOKEN = '669a4c52'
API_URL = 'https://api.vk.com/method/'

# Сюда будем добавлять ID пользователей, которым уже ответили ночью
answered_users = set()

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
        message = data['object']['message']
        user_id = message['from_id']
        peer_id = message['peer_id']

        # Игнорируем системные сообщения от групп/бота
        if user_id != peer_id:
            print("Пропущено системное сообщение.")
            return 'ok', 200

        now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)  # МСК
        current_time = now.time()
        print("Текущее время:", current_time)

        if current_time >= datetime.time(19, 0) or current_time < datetime.time(11, 0):
            if user_id not in answered_users:
                print("Отправляем сообщение пользователю:", user_id)
                send_message(user_id, """Приветствуем Вас! В данный момент магазин закрыт. В рабочее время с Вами свяжется наш менеджер и ответит на Ваши вопросы.
График магазина с 11:00 до 19:00.
Благодарим за понимание!""")
                answered_users.add(user_id)
            else:
                print("Пользователю уже отправляли сообщение ночью, пропускаем.")
        else:
            print("Сейчас рабочее время — бот не отвечает.")

    return 'ok', 200

def send_message(user_id, message):
    response = requests.post(API_URL + 'messages.send', params={
        'user_id': user_id,
        'message': message,
        'random_id': int(time.time()),
        'access_token': TOKEN,
        'v': '5.131'
    })
    print("Ответ от VK:", response.text)

# Фоновый поток для сброса списка в 11:00
def reset_answered_users():
    while True:
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)  # МСК
        if now.time().hour == 11 and now.time().minute == 0:
            answered_users.clear()
            print("Список пользователей сброшен в 11:00")
            time.sleep(60)  # Ждём минуту, чтобы не сбрасывать несколько раз
        time.sleep(1)

# Запускаем сброс в отдельном потоке
threading.Thread(target=reset_answered_users, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)