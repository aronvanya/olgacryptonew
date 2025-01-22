from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# Ваш API ID и API Hash
api_id = 21078867  # Замените на ваш API ID
api_hash = "95e80b6bea78c5b0c5442702c8cc17de"  # Замените на ваш API Hash

# Создаём новую строковую сессию
with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("Ваша строковая сессия:")
    print(client.session.save())
