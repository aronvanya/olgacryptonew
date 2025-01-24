import os
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import threading
import time
import requests
import asyncio

# Настройки API
api_id = 21078867
api_hash = "95e80b6bea78c5b0c5442702c8cc17de"
string_session = "1ApWapzMBu3jCir6F04lSI2Rhzm2hDITwY_z3lNH1jsj1OfwUFVQEEVAjaZcSAv2yPl4FgE3mdWHCvk8SOm8HlG25OHzhAhjd79IrEQA66tPfBSisXnfmxAZyCTvzKkeL9NV44JaG96mVaK1VQG1HujvJp-8yxGHYc4BTyFD_ANr0SnsNEka1ZnXDshX4VRcwAAXd3GFV4wupzo0mhQJ2htWkbHXgNKHk6nW_hUkikbGr0w_m5tgRxXRBbnBBLLi1-p8W87OOJYrEdblWlUEMTZJmLk19LQ466nEgg58dCFlMqszwx9lmB-RHoYsJyGEj1Ol3714OaObFNBlkkyvWqd0ESCxNkWI="
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

# Локальный пинг
def local_ping():
    while True:
        try:
            response = requests.get("http://127.0.0.1:8080/")
            if response.status_code == 200:
                print("Local ping successful!")
            else:
                print(f"Local ping failed with status {response.status_code}.")
        except Exception as e:
            print(f"Error during local ping: {e}")
        time.sleep(60)

# Обработчик сообщений
@client.on(events.NewMessage(chats=source_channel_id))
async def handler(event):
    print(f"Получено сообщение: {event.message.to_dict()}")
    message = event.message
    reply_to = message.reply_to

    if reply_to:
        # Определяем ID раздела
        topic_id = reply_to.reply_to_top_id if reply_to.reply_to_top_id else reply_to.reply_to_msg_id
        print(f"ID раздела: {topic_id}")

        # Проверяем, соответствует ли раздел маппингу
        if topic_id in section_mapping:
            target_topic = section_mapping[topic_id]
            try:
                # Пересылаем сообщение в нужный раздел
                await client.send_message(target_channel_id, message.text, reply_to=target_topic)
                print(f"Сообщение из раздела {topic_id} отправлено в раздел {target_topic}: {message.text}")
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
        else:
            print(f"Пропущено: сообщение из раздела {topic_id}.")
    else:
        print(f"Пропущено: сообщение без reply_to. Полное сообщение: {message.to_dict()}")

# Flask
def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Telegram клиент
def run_telegram_client():
    client.start()
    client.run_until_disconnected()

# Запуск потоков
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

ping_thread = threading.Thread(target=local_ping)
ping_thread.start()

print("Бот запущен. Ожидаем сообщения...")
run_telegram_client()
