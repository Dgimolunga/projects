# -*- coding: utf-8 -*-
from .Bot_test3 import dp
from aiogram.types import Message
from .messages import MESSAGES


@dp.message_handler(commands=["start"])
async def process_start_command(message: Message):
    await message.reply(MESSAGES['start'])

