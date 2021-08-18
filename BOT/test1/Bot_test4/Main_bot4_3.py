# -*- coding: utf-8 -*-
from BOT.test1.Bot_test4 import config_for_bot as cfg
from BOT.test1.Bot_test4 import config_dicts as cfg_d
import telethon
import asyncio


class telega(telethon.TelegramClient):
    def __init__(self, session: 'typing.Union[str, Session]', api_id: int, api_hash: str,
                 loop: asyncio.events.AbstractEventLoop = None):
        super().__init__(session, api_id, api_hash, loop=loop)
        for handler in cfg_d.handlers_USERBOT_dict:
            print(handler)
            self.add_event_handler(cfg_d.handlers_USERBOT_dict[handler])


class telethonBot(telethon.TelegramClient):
    def __init__(self, session: 'typing.Union[str, Session]', api_id: int, api_hash: str,
                 loop: asyncio.events.AbstractEventLoop = None):
        super().__init__(session, api_id, api_hash, loop=loop)
        for handler in cfg_d.handlers_BOT_dict:
            print(handler)
            self.add_event_handler(cfg_d.handlers_BOT_dict[handler])


clients = []
bots = []
botsMain = None
# @telethon.events.register(telethon.events.NewMessage)
# async def event_handler_ms(event):
#     client_event = event.client
#     if event.message and event.message.sender_id != -1001557150106:
#         print(client_event)
#         await client_event.send_message(cfg.my_channel_id, message="!!!!!!!!!!!!!!!!!!NewMessage!!!!!!!!!!!!!!!")


# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)

async def client_run(loop, client_bot=botsMain, sender_id='Dgimolunga2'):
    client = telega("NewClient" + str(cfg.id_), cfg.api_id, cfg.api_hash, loop=loop)
    cfg.id_ += 1
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request("79525362955")
        if client_bot is None:
            client_bot = botsMain
            await client_bot.start()
            await client_bot.connect()
        async with client_bot.conversation(sender_id) as conv:
            await conv.send_message('Enter password?')
            password = await conv.get_response(timeout=100)
            await client.sign_in("79525362955", password)
            await conv.send_message('Nice to meet you, {}!'.format(password.text))
    clients.append(client)
    await client.start()
    await client.run_until_disconnected()


async def BOT_client_run(loop):
    global botsMain
    bot = telethonBot('MainBOT', cfg.api_id, cfg.api_hash, loop=loop)
    bots.append(bot)
    botsMain = bot
    await bot.start(bot_token=cfg.bot_token)
    await bot.run_until_disconnected()


def add_client_to_loop(loop, client_bot=botsMain, sender_id=None):
    loop = asyncio.get_event_loop()
    loop.create_task(client_run(loop, client_bot, sender_id))


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.create_task(BOT_client_run(loop))
    # loop.run_until_complete(client_run(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt as e:
        pass


if __name__ == '__main__':
    main()

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

# loop.run_until_complete(clients[0].r)
# clients[1].add_event_handler(event_handler_ms)
# clients[0].start()
# loop.run_until_complete(clients[0].connect())
# print("CLIENT1 START")
# clients[0].run_until_disconnected()
# print("CLIENT2 START")
# clients[1].run_until_disconnected()
# async def main():
#     task = asyncio.create_task(clients[0].start())
#     await asyncio.gather((task,))
#
#
# if __name__ == '__main__':
# async def main():
#     await clients[0].get
# async def main():
#     await clients[0].connect()
#     await clients[0].idle()   # ends with Ctrl+C
#
# # loop.create_task(main())
# # loop.run_forever()
# #     # pass
# loop.run_until_complete(main())
# -*- coding: utf-8 -*-
