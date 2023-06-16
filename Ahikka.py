from telethon.sync import TelegramClient
from telethon import events
import asyncio

# Конфигурация API
api_id = '20099691'
api_hash = 'ec9f98c39c205e13deefdcd0834a80e5'
session_file = 'sessionally'

# Подключение к Telegram
client = TelegramClient(session_file, api_id, api_hash)
client.start()

# Переменная для хранения состояния дублирования сообщений
duplicate_enabled = True

# Обработчик команды /a
@client.on(events.NewMessage(pattern='/a'))
async def handle_command_a(event):
    # Получение аргументов команды
    args = event.raw_text.split()[1:]  # Пропускаем "/a"
    if len(args) < 2:
        await event.reply('Недостаточно аргументов. Используйте: /a <text> <int>')
        return

    text = args[0]
    interval = int(args[1])

    if interval == 0:
        await event.reply('Значение интервала не может быть 0.')
        return

    global duplicate_enabled

    if text.lower() == 'off':
        if duplicate_enabled:
            duplicate_enabled = False
            await event.reply('Код успешно отключен.')
        else:
            await event.reply('Код уже отключен.')
    else:
        duplicate_enabled = True
        await event.reply('Успешно. Ожидайте {} часов.'.format(interval))

        while duplicate_enabled:
            # Отправка сообщения в текущий чат или диалог
            await event.respond(text)

            await asyncio.sleep(interval * 3600)  # Ожидание заданного количества часов

# Запуск бота
with client:
    client.run_until_disconnected()
