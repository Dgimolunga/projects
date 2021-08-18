# -*- coding: utf-8 -*-
import telethon
from BOT.test1.Bot_test4 import config_for_bot as cfg
from BOT.test1.Bot_test4.Main_bot4_2 import add_client_to_loop


@telethon.events.register(telethon.events.NewMessage(chats=[-1001518950788]))
async def event_handler_ms_from(event):
    client_event = event.client
    if event.message and event.message.sender_id != -1001557150106:
        print(event.message.text)
        await client_event.forward_messages(cfg.my_channel_id, event.message)
        if event.message.text == "132":
            add_client_to_loop()
            print('client connect!: ')
    raise telethon.events.StopPropagation


@telethon.events.register(telethon.events.NewMessage)
async def event_handler_spam_ms(event):
    client_event = event.client
    if event.message and event.message.sender_id not in (-1001509028433, -1001557150106, 1939139289):
        print(event.message.text)
        await client_event.send_message(cfg.my_spam_channel_id, message="!!!SPAM FROM SUB!!!")
