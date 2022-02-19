import os

from pyrogram import Client, filters
from dotenv import load_dotenv, find_dotenv
import requests

app = Client("my_account")

load_dotenv(find_dotenv())
channel_id = int(os.getenv('CHANNEL_ID'))
bot_id = int(os.getenv('BOT_ID'))

@app.on_message()
async def hello(client, message):
    body = {"query": "{\n\t\t\tgetSendChats {\n\t\t\t\tid\n\t\t\t\ttgChatId\n\t\t\t    listen\n\t\t\t}\n\t\t}"}
    res = requests.post('http://127.0.0.1:2000/graphql', json=body)
    send_chats = []
    get_send_chats = res.json()['data']['getSendChats']
    for i in range(len(get_send_chats)):
        send_chats.append(int(get_send_chats[i]['tgChatId']))
    if message.chat.id in send_chats:
        # Если автор сообщения я - выйдем
        if message.channel_chat_created:
            return
        # Наше сообщение, которое мы будем отправлять боту
        text = message.text
        # Если есть текст выполняем код
        if text:
            # Массив значений стиля текста, библиотечка сама рисует так как нужно
            # Отправляем сообщение боту, который потом будет переводить и писать в БД
            await app.send_message(bot_id, text, entities=message.entities)

        photo = message.photo
        caption = message.caption
        if photo:
            await app.send_photo(bot_id, photo=photo.file_id, caption=caption, caption_entities=message.caption_entities)


app.run()
