from telethon.sync import TelegramClient
from telethon import events
import asyncio

# Конфигурация API
api_id = ''
api_hash = ''
session_file = 'sessionally'

#v 1.0.2

# Подключение к Telegram
client = TelegramClient(session_file, api_id, api_hash)
client.start()

# Переменная для хранения состояния дублирования сообщений
duplicate_enabled = True

# Обработчик команды /a
@client.on(events.NewMessage(pattern='/a'))
async def handle_command_a(event):
    # Получение аргументов команды
    args = event.raw_text.split(maxsplit=1)[1:]  # Пропускаем "/a" и получаем максимум один аргумент

    if not args:
        await event.reply('Недостаточно аргументов. Используйте: /a <text> <int>')
        return

    input_text = args[0].strip()

    # Разделение текста на слова
    words = input_text.split()

    if not words or not words[-1].isdigit():
        await event.reply('Недостаточно аргументов. Используйте: /a <text> <int>')
        return

    text = ' '.join(words[:-1])
    interval = int(words[-1])

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

