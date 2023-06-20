from telethon.sync import TelegramClient
from telethon import events
import sys
import asyncio

#v 1.3.4(stable)

if len(sys.argv) < 5:
    print("Недостаточно аргументов. Используйте: python Ahikka.py api_id api_hash user_id language")
    sys.exit(1)

api_id = sys.argv[1]
api_hash = sys.argv[2]
user_id = sys.argv[3]
language = sys.argv[4]
session_file = 'sessionally'

client = TelegramClient(session_file, api_id, api_hash)
client.start()

duplicate_enabled = True

def get_message_text(language, key):
    messages = {
        'EN': {
            'not_enough_args': 'Not enough arguments. Usage: /a "<text>" <int> or /a off',
            'invalid_argument': 'Invalid argument format for <int>. Usage: /a "<text>" <int> or /a off',
            'interval_zero': 'Interval value cannot be 0.',
            'code_disabled': 'Code successfully disabled. To enable it again use /a "<text> "<int>',
            'code_already_disabled': 'Code is already disabled.',
            'success_message': 'Success. Wait for {} hour(s).',
            'off_message': 'Code already disabled.',
            'message_sent': 'Message sent: {}',
            'language_updated': 'Language successfully updated to English.',
            'language_already_set': 'Language is already set to English.'
        },
        'RU': {
            'not_enough_args': 'Недостаточно аргументов. Используйте: /a "<text>" <int> или /a off',
            'invalid_argument': 'Неверный формат аргумента <int>. Используйте: /a "<text>" <int> или /a off',
            'interval_zero': 'Значение интервала не может быть 0.',
            'code_disabled': 'Код успешно отключен. Чтобы его включить заново используйте /a "<text>" <int>',
            'code_already_disabled': 'Код уже отключен.',
            'success_message': 'Успешно. Ожидайте {} час(ов).',
            'off_message': 'Код уже отключен.',
            'message_sent': 'Сообщение отправленно: {}',
            'language_updated': 'Язык успешно изменен на Русский.',
            'language_already_set': 'Язык уже установлен на Русский.'
        }
    }
    return messages[language][key]

@client.on(events.NewMessage(pattern='/a'))
async def handle_command_a(event):
    global duplicate_enabled

    if event.sender_id != int(user_id):
        return

    args = event.raw_text.split()
    if len(args) < 3:
        if len(args) == 2 and args[1].lower() == 'off':
            if duplicate_enabled:
                duplicate_enabled = False
                await event.reply(get_message_text(language, 'code_disabled'))
            else:
                await event.reply(get_message_text(language, 'code_already_disabled'))
        else:
            await event.reply(get_message_text(language, 'not_enough_args'))
        return

    text = ' '.join(args[1:-1]).strip('"')
    number = args[-1]

    try:
        number = int(number)
    except ValueError:
        await event.reply(get_message_text(language, 'invalid_argument'))
        return

    if number == 0:
        await event.reply(get_message_text(language, 'interval_zero'))
        return

    await event.reply(get_message_text(language, 'success_message').format(number))

    while duplicate_enabled:
        await event.reply(text)
        await asyncio.sleep(number * 3600)

@client.on(events.NewMessage(pattern='/language'))
async def handle_command_language(event):
    global language
    args = event.raw_text.split()
    if len(args) != 2:
        return

    new_language = args[1].upper()
    if new_language in ('EN', 'RU'):
        if new_language != language:
            language = new_language
            await event.reply(get_message_text(language, 'language_updated'))
        else:
            await event.reply(get_message_text(language, 'language_already_set'))

with client:
    client.run_until_disconnected()
