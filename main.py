import os
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import threading
import requests

# Настройки API
api_id = 21078867  # Ваш API ID
api_hash = "95e80b6bea78c5b0c5442702c8cc17de"  # Ваш API Hash
string_session = "1ApWapzMBu480WTeHnPyr_MsiPbeabG6UVEHJr67wOp6PYv1em6paWIKpbVNO4QY-eGnI3T_IplUyK7QzZs31nhLy-neLeaQeSy39kBUWKBCSECjN78KjPJz7g9d9R1YMELLCkx4_cpPC41HQQJPIa2jUQTZV0LlRNN3EyOVh3G_ouvW_AUhW1kd-dw49xzV4Opz9GdvAwlFgVYkBrSS6wYDW1T4XlmJdGDw2G-Vwfw34_-2T1xx0CXybl1pnrmVXmfJxepwegQXZ1NLjBYF75tS7ioa1oB-YR7RWyiwEcPMuGdM0lBJEIjiT4ncX_WBzeq4WkWxuAM0VlduuQ9YcoGW3nT4ikDw="

# Данные каналов
source_channel_id = -1002361161091  # ID канала-источника
target_channel_id = -1002324576765  # ID целевой группы

# ID разделов и их соответствия
section_mapping = {
    3: 33,
    5: 29,
    976: 32,
    1986: 35
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
    message = event.message
    reply_to = message.reply_to

    if reply_to:
        topic_id = reply_to.reply_to_top_id if reply_to.reply_to_top_id else reply_to.reply_to_msg_id
        if topic_id in section_mapping:
            target_topic_id = section_mapping[topic_id]
            try:
                await client.send_message(
                    target_channel_id, message.text,
                    reply_to=target_topic_id
                )
                print(f"Сообщение из раздела {topic_id} отправлено в раздел {target_topic_id}: {message.text}")
            except Exception as e:
                print(f"Ошибка при отправке сообщения в раздел {target_topic_id}: {e}")
        else:
            print(f"Пропущено: сообщение из раздела {topic_id}")
    else:
        print(f"Пропущено: сообщение без reply_to. Полное сообщение: {message.to_dict()}")

# Запуск Flask в отдельном потоке
def run_flask():
    port = int(os.environ.get("PORT", 8080))  # Используем порт, предоставленный Heroku
    app.run(host="0.0.0.0", port=port)

# Запуск пинга самого себя для поддержания активности
def ping_self():
    while True:
        try:
            requests.get("http://127.0.0.1:8080")
            print("Local ping successful!")
        except Exception as e:
            print(f"Ошибка пинга: {e}")
        threading.Event().wait(60)  # Пинг раз в минуту

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

ping_thread = threading.Thread(target=ping_self)
ping_thread.start()

# Запуск Telegram клиента
def run_telegram_client():
    print("Бот запущен. Ожидаем новые сообщения...")
    client.start()
    client.run_until_disconnected()

telegram_thread = threading.Thread(target=run_telegram_client)
telegram_thread.start()
