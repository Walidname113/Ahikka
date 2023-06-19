from telethon.sync import TelegramClient
from telethon import events
import asyncio
import sys

#v 1.1.5

# Проверка наличия аргументов в команде
if len(sys.argv) < 4:
    print("Недостаточно аргументов. Используйте: python Ahikka.py api_id api_hash user_id")
    sys.exit(1)

# Извлечение аргументов из командной строки
api_id = sys.argv[1]
api_hash = sys.argv[2]
user_id = sys.argv[3]
session_file = 'sessionally'

# Подключение к Telegram
client = TelegramClient(session_file, api_id, api_hash)
client.start()

# Переменная для хранения состояния дублирования сообщений
duplicate_enabled = True

#  /a
@client.on(events.NewMessage(pattern='/a'))
async def handle_command_a(event):
    # Проверка, что команду отправил только указанный пользователь
    if event.sender_id != int(user_id):
        return

    # Получение аргументов команды
    args = event.raw_text.split()
    if len(args) < 3:
        await event.reply('Недостаточно аргументов. Используйте: /a "<text>" <int> или /a off')
        return

    if len(args) == 2 and args[1].lower() == 'off':
        global duplicate_enabled
        if duplicate_enabled:
            duplicate_enabled = False
            await event.reply('Код успешно отключен.')
        else:
            await event.reply('Код уже отключен.')
    else:
        text = ' '.join(args[1:-1]).strip('"')
        number = args[-1]

        try:
            number = int(number)
        except ValueError:
            await event.reply('Неверный формат аргумента <int>. Используйте: /a "<text>" <int> или /a off')
            return

        if number == 0:
            await event.reply('Значение интервала не может быть 0.')
            return

        await event.reply('Успешно. Ожидайте {} часов.'.format(number))

        while duplicate_enabled:
            # Отправка сообщения в текущий чат или диалог
            await event.respond(text)

            await asyncio.sleep(number * 3600)  # Ожидание заданного количества часов

# Запуск бота
with client:
    client.run_until_disconnected()
