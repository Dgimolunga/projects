# -*- coding: utf-8 -*-
from telethon import TelegramClient, events, utils
import config_for_bot as cfg
import BOT.test1.config_for_bot as cfg
import threading
import re
import telebot
import PIL
from PIL import Image
from requests import get
import requests
import aiogram
import asyncio
from aiogram.types import Message
import threading
import time

lock = threading.Lock()
stop_thread = False

password = None
loop = asyncio.get_event_loop()
bot = aiogram.Bot('1939139289:AAFVpUsGo1YmGz5VX4o7BwR77M1Ic99yJ9k', parse_mode="HTML")
dp = aiogram.Dispatcher(bot, loop=loop)


@dp.message_handler(commands=['start'])
async def process_start_command(message: Message):
    await message.reply("Привет!\nНапиши мне /set_api_hash_and_id your_api_hash !")


@dp.message_handler(commands=['set_api_hash_and_id'])
async def process_start_command(message: Message):
    cfg.api_hash, cfg.api_id = message.text.split()[1:]
    await message.reply(f"Данные сохранены!{cfg.api_id} and {cfg.api_hash}")


@dp.message_handler(commands=['set_id_channel'])
async def process_start_command(message: Message):
    cfg.my_channel_id = message.text.split()[1]
    await message.reply(f"Данные сохранены!{cfg.my_channel_id}")


@dp.message_handler(commands=['set_id_channel'])
async def process_start_command(message: Message):
    cfg.my_channel_id = message.text.split()[1]
    await message.reply(f"Данные сохранены!{cfg.my_channel_id}")


@dp.message_handler(commands=['start_script'])
async def process_start_command(message: Message):
    if all((cfg.api_hash, cfg.api_id, cfg.my_channel_id)):
        thread = threading.Thread(target=main1, args=())
        thread.start()

    await message.reply(f"Запущено!")


@dp.message_handler(commands=['stop_script'])
async def process_start_command(message: Message):
    lock.acquire()
    global stop_thread
    stop_thread = True
    lock.release()
    await message.reply(f" disЗапущено!")


# @dp.message_handler1()
# async def send_mes():
#     await bot.send_message(chat_id=c, text=text)


@dp.message_handler()
async def echo(message: Message):
    global password
    if all((cfg.api_hash, cfg.api_id, cfg.my_channel_id)):
        print("!!!!!!!!!!!!!!!!!!")
        password = message.text
    text = f'You write{message.text}'
    await bot.send_message(chat_id=message.from_user.id, text=text)
    await message.answer(text=text)


async def main():
    global password
    client = TelegramClient("Test2", cfg.api_id, cfg.api_hash)
    print("sd")
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request("79525362955")
        while True:
            if password:
                break
            time.sleep(0.1)

        # request = requests.get("https://api.telegram.org/bot1939139289:AAFVpUsGo1YmGz5VX4o7BwR77M1Ic99yJ9k/sendMessage?chat_id=736020250&text=Введите пароль для авторизации")
        # while True:
        #     get_pass_req = requests.get("https://api.telegram.org/bot1939139289:AAFVpUsGo1YmGz5VX4o7BwR77M1Ic99yJ9k/getUpdates?offset=-1").json()
        #     if get_pass_req["result"] != []:
        #         break
        #     time.sleep(0.5)
        #     print(get_pass_req)
        # get_pass = get_pass_req["result"][0]["message"]["text"]
        # print(get_pass_req)
        # a = input("Cod ?")
        await client.sign_in("79525362955", password)

    @client.on(events.NewMessage)
    async def my_handler_message(event):
        if stop_thread is True:
            await client.disconnect()
        print("!!!!1111", stop_thread, threading.get_ident())
        await client.forward_messages(cfg.my_channel_id, event.message)
        pass


    await client.start()
    await client.run_until_disconnected()


def main1():
    stop_thread = False
    asyncio.run(main())


api_id = cfg.api_id
api_hash = cfg.api_hash
my_channel_id = cfg.my_channel_id
channels = cfg.channels
patterns = cfg.patterns  # sql
aiogram.executor.start_polling(dp)




