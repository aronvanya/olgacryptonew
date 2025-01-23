from telethon import TelegramClient, events
from telethon.sessions import StringSession
import logging
import os

# Логирование
logging.basicConfig(level=logging.INFO)

# Настройки API
api_id = 21078867
api_hash = "95e80b6bea78c5b0c5442702c8cc17de"
string_session = "1ApWapzMBu480WTeHnPyr_MsiPbeabG6UVEHJr67wOp6PYv1em6paWIKpbVNO4QY..."

# Данные каналов
source_channel_id = -1002361161091
target_channel_id = -1002324576765
allowed_topics = [3, 5, 6, 976, 1986, 736]

# Инициализация Telegram клиента
client = TelegramClient(StringSession(string_session), api_id, api_hash)

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
        logging.info(f"Пропущено: сообщение без reply_to. Полное сообщение: {message.to_dict()}")

if __name__ == "__main__":
    logging.info("Бот запущен. Ожидаем новые сообщения...")
    client.start()
    client.run_until_disconnected()
