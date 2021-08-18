# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from BOT.test1.Bot_test4 import config_for_bot as cfg
from BOT.test1.Bot_test4 import config_dicts as cfg_d
import telethon
import asyncio


# @telethon.events.register(telethon.events.NewMessage)
# async def event_handler_ms(event):
#     client_event = event.client
#     if event.message and event.message.sender_id != -1001557150106:
#         print(client_event)
#         await client_event.send_message(cfg.my_channel_id, message="!!!!!!!!!!!!!!!!!!NewMessage!!!!!!!!!!!!!!!")


class Telega(telethon.TelegramClient):
    def __init__(self, session: 'typing.Union[str, Session]', api_id: int, api_hash: str):
        super().__init__(session, api_id, api_hash)
        for handler in cfg_d.handlers_USERBOT_dict:
            print(handler)
            self.add_event_handler(cfg_d.handlers_USERBOT_dict[handler])



# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
clients = []
for i in range(2):
    clients.append(Telega("NewClient" + str(i), cfg.api_id, cfg.api_hash))


# client1 = telethon.TelegramClient("NewClient1", cfg.api_id, cfg.api_hash)
# client2 = telethon.TelegramClient("NewClient2", cfg.api_id, cfg.api_hash)

# a = clients[1]

# def iter(fun):
#
#     for client in clients:
#         @client.on(telethon.events.NewMessage())
#         async def funcal(event):
#             await fun(event)






# @a.on(telethon.events.NewMessage())
# async def my_event_handler(event):
#     if event.message and event.message.sender_id != -1001557150106:
#         print("@@@@@@@@@APPLE")
#         await clients[0].send_message(cfg.my_channel_id, message="@@@@@@@@@@@@@@APpLE")
# @iter
# async def my_event_handler1(event):
#     if event.message and event.message.sender_id != -1001557150106:
#         print(event.client)
#         if event.message.text == '132':
#             clients.append(telethon.TelegramClient("NewClient!!!" + str(22), cfg.api_id, cfg.api_hash))
#             clients[2].add_event_handler(my_event_handler1, telethon.events.NewMessage())
#             await clients[2].start()
#             await clients[2].run_until_disconnected()
#         await clients[0].send_message(cfg.my_channel_id, message="!!!!!!!!!!!!!!APpLE")
#
# clients[1].add_event_handler(event_handler_ms)


clients[0].start()
clients[1].start()
print("CLIENT1 START")
clients[0].run_until_disconnected()
print("CLIENT2 START")
clients[1].run_until_disconnected()
if __name__ == '__main__':
    pass
    # asyncio.run(main())
