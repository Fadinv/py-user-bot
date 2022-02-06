from pyrogram import Client, filters

app = Client("my_account")


@app.on_message()
async def hello(client, message):
    me = await app.get_me()
    # Если автор сообщения я - выйдем
    if message.from_user and message.from_user.id == me.id:
        return
    # Говнокод, надо разобраться, как безопасно сделать эту проверку
    if message.chat.id == int(app.config_file.CHANNEL_ID):
        return
    if message.chat.id == int(app.config_file.BOT_ID):
        return
    # Если это уведомление о созданном канале выходим
    if message.channel_chat_created:
        return
    # Наше сообщение, которое мы будем отправлять боту
    text = message.text
    # Если есть текст выполняем код
    if text:
        # Массив значений стиля текста, библиотечка сама рисует так как нужно
        # Отправляем сообщение боту, который потом будет переводить и писать в БД
        await app.send_message(int(app.config_file.BOT_ID), text, entities=message.entities)


app.run()
