# -*- coding: utf-8 -*-
from telethon import TelegramClient, events
import asyncio
from BOT.test1.Bot_test4 import config_for_bot as cfg
import time

bot = TelegramClient('bot', cfg.api_id, cfg.api_hash)


@bot.on(events.NewMessage(pattern='/start'))
async def send_welcome(event):
    print('/start' in event.message.text)
    client = event.client
    print(event.sender_id)
    arg = event.message.text.split()[1]
    a = 2
    if a == 2:
        try:
            a = await client.get_peer_id(arg)
        except:
            return
        print(a)
    await client.send_message(736020250, message="!!!!!!!!!!!!!!!!!!send message!!!!!!!!!!!!")
    async with event.client.conversation(event.sender_id) as conv:
        await conv.send_message('Hey, what is your name?')

        response = await conv.get_response()
        name = response.text

        await conv.send_message('Nice to meet you, {}!'.format(name))


bot.start(bot_token=cfg.bot_token)
bot.run_until_disconnected()
# -*- coding: utf-8 -*-
