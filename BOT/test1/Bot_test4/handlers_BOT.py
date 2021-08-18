# -*- coding: utf-8 -*-
import telethon
from BOT.test1.Bot_test4 import config_for_bot as cfg
from BOT.test1.Bot_test4.Main_bot4_3 import add_client_to_loop
import re
# ______________________________________________________________________________________________________________________

from BOT.test1.Bot_test4.bot_database import set_data, get_data, NotCorrect, DataDuplicateExc
from BOT.test1.Bot_test4.bot_database import command_get_list, command_set_list, arg_other, arg_for_session
import logging

# from BOT.test1.Bot_test4 import test_sqlalchemy


@telethon.events.register(telethon.events.NewMessage(pattern='/start'))
async def BOT_handler_start(event):
    await event.reply('Howdy, how are you doing?')
    raise telethon.events.StopPropagation


# @telethon.events.register(telethon.events.NewMessage(pattern='/set_api_hash_and_api_id'))
# async def BOT_handler_set_api_hash_and_id(event):
#     api_hash, api_id = event.message.text.split()[1:3]
#
#     re_id = re.findall(r'^[0-9]+', api_id)
#     if not (''.join(re_id) == api_id):
#         await event.reply('Неверный формат api_id')
#         raise telethon.events.StopPropagation
#         return
#     print(api_hash)
#     re_hash = re.findall(r'^[a-zA-Z0-9]+', api_hash)
#     print(re_hash)
#     if not (''.join(re_hash) == api_hash):
#         await event.reply('Неверный формат api_hash')
#         raise telethon.events.StopPropagation
#         return
#
#     set_data(event.sender_id, api_hash=api_hash, api_id=int(api_id))
#     await event.reply(f"Данные сохранены!{api_hash} and {api_id}")
#     raise telethon.events.StopPropagation


# @telethon.events.register(telethon.events.NewMessage(pattern='/set_phone_number'))
# async def BOT_handler_set_phone_number(event):
#     phone_number = event.message.text.split()[1]
#
#     re_id = re.findall(r'^[0-9]+', phone_number)
#     if not (''.join(re_id) == phone_number):
#         await event.reply('Неверный формат ')
#         raise telethon.events.StopPropagation
#         return
#     set_data(event.sender_id, phone=phone_number)
#     await event.reply(f"Данные сохранены!{phone_number}")
#     raise telethon.events.StopPropagation

# @telethon.events.register(telethon.events.NewMessage(pattern='/set_id_share_channel'))
# async def BOT_handler_set_id_channel(event):
#     id_share_channel = event.message.text.split()[1]
#
#     re_id = re.findall(r'^[0-9]+', id_share_channel)
#     if not (''.join(re_id) == id_share_channel):
#         try:
#             id_share_channel = await event.client.get_peer_id(id_share_channel)
#         except:
#             await event.reply('Неверный формат api_id')
#             raise telethon.events.StopPropagation
#             return
#
#     set_data(event.sender_id, share_channel_id=int(id_share_channel))
#     await event.reply(f"Данные сохранены!{id_share_channel}")
#     raise telethon.events.StopPropagation

@telethon.events.register(telethon.events.NewMessage(pattern='/set'))
async def BOT_handler_set_data(event):
    try:
        list_ = event.message.text.split(maxsplit=2)
        if len(list_) < 2:
            raise NotCorrect
        set__, data = list_[0:2]
        setlist_ = list_[0].split('_', maxsplit=2)
        if len(setlist_) < 3:
            raise NotCorrect
        _, session_name, arg = setlist_

        set_data(event.sender_id, session_name, arg, data)
        await event.reply(f"Данные сохранены: session '{session_name}':{arg}: {data}")
    except NotCorrect as e:
        await event.reply('{}\n'
                          'Введена неправильная команда.\nExample: "/set_sessionname_*** value"\n*** - one of:\n{} for '
                          'start script;\n{} for other set'.format(e, arg_for_session, arg_other))
    except:
        await event.reply('Что-то пошло не так')
        raise
    finally:
        raise telethon.events.StopPropagation


@telethon.events.register(telethon.events.NewMessage(pattern='/get'))
async def BOT_handler_get_data(event):
    try:
        getlist_ = event.message.text.split(maxsplit=1)[0].split('_', maxsplit=2)
        if len(getlist_) < 3:
            raise NotCorrect
        _, session_name, arg = getlist_

        value_arg = get_data(event.sender_id, session_name, arg)
        await event.reply("session '{}':{}:: {}".format(session_name, arg, value_arg))
    except NotCorrect as e:
        await event.reply('{}\nВведена неправильная команда.\n'
                          'Example: "/get_sessionname_***"\n*** - one of:\n {}'.format(e, command_get_list))
    except:
        await event.reply('Что-то пошло не так')
        raise
    finally:
        raise telethon.events.StopPropagation


@telethon.events.register(telethon.events.NewMessage(pattern='/add'))
async def BOT_handler_add_data(event):
    try:
        list_ = event.message.text.split()
        if len(list_) < 2:
            raise NotCorrect
        add__, data = list_[0], list_[1:]
        addlist_ = add__.split('_', maxsplit=2)
        if len(addlist_) != 3:
            raise NotCorrect
        _, session_name, arg = addlist_

        for i in data:
            set_data(event.sender_id, session_name, arg, i)
        await event.reply(f"Данные сохранены: session '{session_name}':{arg}: {data}")
    except NotCorrect as e:
        await event.reply('{}\nВведена неправильная команда.\n'
                          'Example: "/add_sessionname_*** value"\n*** - one of:\n{}'.format(e, arg_for_session,
                                                                                            arg_other))
    except DataDuplicateExc as e:
        await event.reply(f'{e}')
    except:
        await event.reply('Что-то пошло не так')
        raise
    finally:
        raise telethon.events.StopPropagation


@telethon.events.register(telethon.events.NewMessage(pattern='/start_script'))
async def BOT_handler_start_script(event):
    if all((cfg.api_hash, cfg.api_id, cfg.my_channel_id)):
        add_client_to_loop(event.client, event.sender_id)
        await event.reply(f"Запущено!")
    raise telethon.events.StopPropagation


@telethon.events.register(telethon.events.NewMessage)
async def BOT_handler_echo(event):
    await event.reply(event.text)
