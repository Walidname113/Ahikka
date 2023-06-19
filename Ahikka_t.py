from telethon.sync import TelegramClient
from telethon import events
import asyncio
import sys

#v 1.1.8

if len(sys.argv) < 4:
    print("Недостаточно аргументов. Используйте: python Ahikka.py api_id api_hash user_id")
    sys.exit(1)

api_id = sys.argv[1]
api_hash = sys.argv[2]
user_id = sys.argv[3]
session_file = 'sessionally'

client = TelegramClient(session_file, api_id, api_hash)
client.start()

user_messages = {}
duplicate_enabled = True

@client.on(events.NewMessage(pattern='/a'))
async def handle_command_a(event):
    if event.sender_id != int(user_id):
        return

    args = event.raw_text.split()
    if len(args) < 3:
        if len(args) == 2 and args[1].lower() == 'off':
            if duplicate_enabled:
                duplicate_enabled = False
                await event.reply('Код успешно отключен.')
            else:
                await event.reply('Код уже отключен.')
        else:
            await event.reply('Недостаточно аргументов. Используйте: /a "<text>" <int> или /a off')
        return

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

    if duplicate_enabled:
        await event.reply(f'Успешно. Ожидайте {number} часов.')

        while duplicate_enabled:
            await event.reply(text)

            await asyncio.sleep(number * 3600)
    else:
        await event.reply('Код уже отключен.')

with client:
    client.run_until_disconnected()
