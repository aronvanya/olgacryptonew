import os
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import logging
import threading

# Настройки API
api_id = 21078867  # Ваш API ID
api_hash = "95e80b6bea78c5b0c5442702c8cc17de"  # Ваш API Hash
session_name = "session_user"  # Имя файла сессии

# Строковая сессия
string_session = "ВАША_СТРОКОВАЯ_СЕССИЯ"

# Инициализация клиента с использованием строковой сессии
client = TelegramClient(StringSession(string_session), api_id, api_hash)

# Данные каналов
source_channel_id = int(os.getenv("SOURCE_CHANNEL_ID"))
target_channel_id = int(os.getenv("TARGET_CHANNEL_ID"))

# ID разделов, которые нужно пересылать
allowed_topics = [3, 5, 6, 976, 1986, 736]

# Настройка Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Bot is running!"

# Обработчик новых сообщений
@client.on(events.NewMessage(chats=source_channel_id))
async def handler(event):
    message = event.message
    reply_to = message.reply_to

    if reply_to:
        topic_id = reply_to.reply_to_top_id if reply_to.reply_to_top_id else reply_to.reply_to_msg_id
        if topic_id in allowed_topics:
            try:
                await client.send_message(target_channel_id, message.text)
                logging.info(f"Сообщение из раздела {topic_id} отправлено: {message.text}")
            except Exception as e:
                logging.error(f"Ошибка при отправке сообщения: {e}")
        else:
            logging.info(f"Пропущено: сообщение из раздела {topic_id}")
    else:
        logging.info(f"Пропущено: сообщение без reply_to")

# Функция для запуска Flask в отдельном потоке
def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Запуск Flask в отдельном потоке
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Запуск клиента
logging.info("Бот запущен. Ожидаем новые сообщения...")
client.start()
client.run_until_disconnected()
