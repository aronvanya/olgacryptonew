import os
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import requests
import asyncio
import threading
import time

# Настройки API
api_id = 21078867
api_hash = "95e80b6bea78c5b0c5442702c8cc17de"
string_session = "1ApWapzMBu480WTeHnPyr_MsiPbeabG6UVEHJr67wOp6PYv1em6paWIKpbVNO4QY-eGnI3T_IplUyK7QzZs31nhLy-neLeaQeSy39kBUWKBCSECjN78KjPJz7g9d9R1YMELLCkx4_cpPC41HQQJPIa2jUQTZV0LlRNN3EyOVh3G_ouvW_AUhW1kd-dw49xzV4Opz9GdvAwlFgVYkBrSS6wYDW1T4XlmJdGDw2G-Vwfw34_-2T1xx0CXybl1pnrmVXmfJxepwegQXZ1NLjBYF75tS7ioa1oB-YR7RWyiwEcPMuGdM0lBJEIjiT4ncX_WBzeq4WkWxuAM0VlduuQ9YcoGW3nT4ikDw="

# Данные каналов
source_channel_id = -1002361161091
target_channel_id = -1002324576765

# Соответствие разделов
section_mapping = {
    3: 33,
    5: 29,
    976: 32,
    1986: 35,
}

# Инициализация Telegram клиента
client = TelegramClient(StringSession(string_session), api_id, api_hash)

# Настройка Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# Обработчик новых сообщений
@client.on(events.NewMessage(chats=source_channel_id))
async def handler(event):
    try:
        message = event.message
        reply_to = message.reply_to

        print(f"Новое сообщение: {message.text}")
        if reply_to:
            topic_id = reply_to.reply_to_top_id if reply_to.reply_to_top_id else reply_to.reply_to_msg_id
            if topic_id in section_mapping:
                target_topic = section_mapping[topic_id]
                await client.send_message(target_channel_id, message.text)
                print(f"Сообщение из раздела {topic_id} отправлено в раздел {target_topic}: {message.text}")
            else:
                print(f"Пропущено: сообщение из раздела {topic_id}")
        else:
            print(f"Пропущено: сообщение без reply_to. Полное сообщение: {message.to_dict()}")
    except Exception as e:
        print(f"Ошибка в обработчике сообщений: {e}")

# Функция для самопинга
def ping_self():
    while True:
        try:
            response = requests.get("http://127.0.0.1:8080")
            if response.status_code == 200:
                print("Самопинг успешен!")
        except Exception as e:
            print(f"Ошибка пинга: {e}")
        time.sleep(60)

# Запуск Flask в главном потоке
def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Запуск Telegram клиента в asyncio
def run_telegram_client():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    with client:
        loop.run_until_complete(client.run_until_disconnected())

# Основной поток для Flask
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Поток для Telegram клиента
telegram_thread = threading.Thread(target=run_telegram_client)
telegram_thread.daemon = True
telegram_thread.start()

# Поток для пинга
ping_thread = threading.Thread(target=ping_self)
ping_thread.daemon = True
ping_thread.start()

print("Бот запущен. Ожидаем новые сообщения...")
telegram_thread.join()
