# -*- coding: utf-8 -*-
from telethon import TelegramClient, events, utils
import config_for_bot as cfg
import BOT.test1.config_for_bot as cfg
import threading
import asyncio
import re

api_id = cfg.api_id
api_hash = cfg.api_hash
my_channel_id = cfg.my_channel_id
channels = cfg.channels
patterns = cfg.patterns  # sql


def main(name, my_channel_id=my_channel_id):

    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    client = TelegramClient('myGrab' + name, api_id, api_hash)  # loop=loop
    # await client.connect()
    # if not await client.is_user_authorized():
    #     await client.send_code_request("79525362955")
    #     await client.sign_in("79525362955", input('Enter the code: '))

    @client.on(events.NewMessage)
    async def my_event_handler(event):

        if all((event.message, event.message.sender_id in channels)):
            if event.message.reply_to:
                reply_msg = await event.message.get_reply_message()
                text_for_search = " ".join((event.message.text.upper(), reply_msg.text.upper()))
            else:
                text_for_search = event.message.text.upper()
            # search pattern in message
            for pattern in patterns:
                if pattern in text_for_search:
                    print(event.message)
                    await client.forward_messages(my_channel_id, event.message)  # share message
                    if event.message.reply_to:
                        await client.send_message(my_channel_id, reply_msg)
                    break

    client.start()
    client.run_until_disconnected()


main("COOL")

# for i in range(2):
#     inp = input("Input ")
#     if inp == "yes":
#         break
#     else:
#
#         print("Client on")
#         thread1 = threading.Thread(target=main, args=(inp,))
#         thread1.start()
