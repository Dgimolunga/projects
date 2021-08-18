# -*- coding: utf-8 -*-
import logging

from BOT.test1.Bot_test3 import config_for_bot as cfg
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
import aiogram
from aiogram.utils import executor
from aiogram.types import Message
from BOT.test1.Bot_test3.messages import MESSAGES
from BOT.test1.Bot_test3.utils import *

# logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
#                     level=logging.DEBUG)

bot = aiogram.Bot(cfg.bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=["start"])
async def process_start_command(message: Message):
    await message.reply(MESSAGES['start'])


@dp.message_handler(commands=["help"])
async def process_help_command(message: Message):
    await message.reply(MESSAGES['help'])


@dp.message_handler(state="*", commands=['setstate'])
async def process_setstate_command(message: Message):
    argument = message.get_args()
    print(argument)
    state = dp.current_state(user=message.from_user.id)
    if not argument:
        await state.reset_state()
        return await message.reply(MESSAGES['state_reset'])

    if (not argument.isdigit()) or (not int(argument) < len(TestStates.all())):
        return await message.reply(MESSAGES['invalid_key'].format(key=argument))

    await state.set_state(TestStates.all()[int(argument)])
    await message.reply(MESSAGES['state_change'], reply=False)


@dp.message_handler(state=TestStates.TESTS_STATES_1)
async def first_test_state_case_met(message: Message):
    await message.reply('First state!', reply=False)


@dp.message_handler(state=TestStates.TESTS_STATES_2[0])
async def second_test_state_case_met(message: Message):
    await message.reply('Second state!', reply=False)


@dp.message_handler(state=TestStates.all())
async def some_test_state_case_met(message: Message):
    state = dp.current_state(user=message.from_user.id)
    text = MESSAGES['current_state'].format(current_state=await state.get_state(), states=TestStates.all())

    await message.reply(text, reply=False)


@dp.message_handler()
async def echo_message(message: Message):
    await bot.send_message(message.from_user.id, message.text)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == "__main__":
    executor.start_polling(dp, on_shutdown=shutdown)
