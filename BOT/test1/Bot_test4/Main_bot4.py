# -*- coding: utf-8 -*-
from BOT.test1.Bot_test4 import config_for_bot as cfg

import telethon
import asyncio

# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
clients = []
for i in range(2):
    clients.append(telethon.TelegramClient("NewClient" + str(i), cfg.api_id, cfg.api_hash))


# client1 = telethon.TelegramClient("NewClient1", cfg.api_id, cfg.api_hash)
# client2 = telethon.TelegramClient("NewClient2", cfg.api_id, cfg.api_hash)

a = clients[1]
def iter(fun):

    for client in clients:
        @client.on(telethon.events.NewMessage())
        async def funcal(event):
            await fun(event)




# @a.on(telethon.events.NewMessage())
# async def my_event_handler(event):
#     if event.message and event.message.sender_id != -1001557150106:
#         print("@@@@@@@@@APPLE")
#         await clients[0].send_message(cfg.my_channel_id, message="@@@@@@@@@@@@@@APpLE")
# @iter
async def my_event_handler1(event):
    if event.message and event.message.sender_id != -1001557150106:
        print(event.client)
        if event.message.text == '132':
            clients.append(telethon.TelegramClient("NewClient!!!" + str(22), cfg.api_id, cfg.api_hash))
            clients[2].add_event_handler(my_event_handler1, telethon.events.NewMessage())
            await clients[2].start()
            await clients[2].run_until_disconnected()
        await clients[0].send_message(cfg.my_channel_id, message="!!!!!!!!!!!!!!APpLE")

a.add_event_handler(my_event_handler1, telethon.events.NewMessage())
clients[0].add_event_handler(my_event_handler1, telethon.events.NewMessage())

clients[0].start()
clients[1].start()
print("sdf")
clients[0].run_until_disconnected()
clients[1].run_until_disconnected()
if __name__ == '__main__':
    pass
    # asyncio.run(main())
