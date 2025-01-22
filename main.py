from telethon import TelegramClient, events
import os

# Настройки API
api_id = int(os.getenv("API_ID"))  # Получение API ID из переменной окружения
api_hash = os.getenv("API_HASH")  # Получение API Hash из переменной окружения
session_name = "session_user"  # Имя файла сессии

# Данные каналов
source_channel_id = int(os.getenv("SOURCE_CHANNEL_ID"))  # ID канала-источника
target_channel_id = int(os.getenv("TARGET_CHANNEL_ID"))  # ID целевой группы

# ID разделов, которые нужно пересылать
allowed_topics = [3, 5, 6, 976, 1986, 736]  # Указанные ID разделов

# Инициализация клиента
client = TelegramClient(session_name, api_id, api_hash)

# Обработчик новых сообщений
@client.on(events.NewMessage(chats=source_channel_id))
async def handler(event):
    # Получаем информацию о сообщении
    message = event.message
    reply_to = message.reply_to

    # Проверяем наличие reply_to
    if reply_to:
        # Используем reply_to_top_id, если доступно
        topic_id = reply_to.reply_to_top_id if reply_to.reply_to_top_id else reply_to.reply_to_msg_id

        # Проверяем, относится ли сообщение к нужным разделам
        if topic_id in allowed_topics:
            try:
                await client.send_message(target_channel_id, message.text)
                print(f"Сообщение из раздела {topic_id} отправлено: {message.text}")
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
        else:
            print(f"Пропущено: сообщение из раздела {topic_id}")
    else:
        print(f"Пропущено: сообщение без reply_to. Полное сообщение: {message.to_dict()}")

# Запуск клиента
print("Бот запущен. Ожидаем новые сообщения...")
client.start()
client.run_until_disconnected()
