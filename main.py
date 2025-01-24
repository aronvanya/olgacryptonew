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
string_session = "1ApWapzMBu3jCir6F04lSI2Rhzm2hDITwY_z3lNH1jsj1OfwUFVQEEVAjaZcSAv2yPl4FgE3mdWHCvk8SOm8HlG25OHzhAhjd79IrEQA66tPfBSisXnfmxAZyCTvzKkeL9NV44JaG96mVaK1VQG1HujvJp-8yxGHYc4BTyFD_ANr0SnsNEka1ZnXDshX4VRcwAAXd3GFV4wupzo0mhQJ2htWkbHXgNKHk6nW_hUkikbGr0w_m5tgRxXRBbnBBLLi1-p8W87OOJYrEdblWlUEMTZJmLk19LQ466nEgg58dCFlMqszwx9lmB-RHoYsJyGEj1Ol3714OaObFNBlkkyvWqd0ESCxNkWI="

# Данные каналов
source_channel_id = -1002361161091  # ID группы-источника
target_channel_id = -1002324576765  # ID целевой группы

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

        if reply_to:
            topic_id = reply_to.reply_to_top_id if reply_to.reply_to_top_id else reply_to.reply_to_msg_id
            if topic_id in section_mapping:
                target_topic = section_mapping[topic_id]
                await client.send_message(target_channel_id, message.text, reply_to=target_topic)
                print(f"Сообщение из раздела {topic_id} отправлено в раздел {target_topic}: {message.text}")
            else:
                print(f"Пропущено: сообщение из раздела {topic_id}")
        else:
            print(f"Пропущено: сообщение без reply_to. Полное сообщение: {message.to_dict()}")
    except Exception as e:
        print(f"Ошибка при обработке сообщения: {e}")

# Дебаг-обработчик для всех новых сообщений
@client.on(events.NewMessage)
async def debug_handler(event):
    print(f"Новое сообщение из чата {event.chat_id}: {event.message.text}")

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
