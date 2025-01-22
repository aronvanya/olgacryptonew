from telethon import TelegramClient, events
import os

# Настройки API
api_id = 21078867  # Ваш API ID
api_hash = "95e80b6bea78c5b0c5442702c8cc17de"  # Ваш API Hash
session_name = "session_user"  # Имя файла сессии

# Строковая сессия, вставьте сюда вашу строку сессии
string_session = "1ApWapzMBu480WTeHnPyr_MsiPbeabG6UVEHJr67wOp6PYv1em6paWIKpbVNO4QY-eGnI3T_IplUyK7QzZs31nhLy-neLeaQeSy39kBUWKBCSECjN78KjPJz7g9d9R1YMELLCkx4_cpPC41HQQJPIa2jUQTZV0LlRNN3EyOVh3G_ouvW_AUhW1kd-dw49xzV4Opz9GdvAwlFgVYkBrSS6wYDW1T4XlmJdGDw2G-Vwfw34_-2T1xx0CXybl1pnrmVXmfJxepwegQXZ1NLjBYF75tS7ioa1oB-YR7RWyiwEcPMuGdM0lBJEIjiT4ncX_WBzeq4WkWxuAM0VlduuQ9YcoGW3nT4ikDw="

# Инициализация клиента с использованием строковой сессии
client = TelegramClient(session_name, api_id, api_hash).start(session=string_session)

# Данные каналов
source_channel_id = int(os.getenv("SOURCE_CHANNEL_ID"))  # ID канала-источника
target_channel_id = int(os.getenv("TARGET_CHANNEL_ID"))  # ID целевой группы

# ID разделов, которые нужно пересылать
allowed_topics = [3, 5, 6, 976, 1986, 736]  # Указанные ID разделов

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
client.run_until_disconnected()
