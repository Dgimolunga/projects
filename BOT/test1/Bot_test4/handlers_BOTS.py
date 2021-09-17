# -*- coding: utf-8 -*-
from __future__ import annotations
import BOT.test1.Bot_test4.logger as my_logger

import telethon
import hashlib
import BOT.test1.Bot_test4.config_for_bot as cfg
from BOT.test1.Bot_test4.data_value import telegram_parse
import asyncio
import re
from asyncio.exceptions import TimeoutError as AIOTimeoutError
# ______________________________________________________________________________________________________________________
# import function of database
from BOT.test1.Bot_test4.bot_database import get_all_users, set_data, get_data, check_user_logging_name, new_user
# import exception of database
from BOT.test1.Bot_test4.bot_database import NotCorrectExc, DataDuplicateExc, UserNotFoundExc
# import var of database
from BOT.test1.Bot_test4.bot_database import command_get_list, command_set_list, arg_other, arg_for_session

command_dict = {
    'add_user': '/add_user',
    'my_users': '/my_users'
}


# _____________________________________________________________________________________________________________________
# @decorator functions

def fsm_decor(action: ActionForFSM):
    def callback(fun):
        def call(*args, **kwargs):
            return parse_bot_users_state_fsm.action_manager(action, fun, args, kwargs)

        return call

    return callback


# _____________________________________________________________________________________________________________________
# FSM classes

class State:
    current_state = None

    @property
    def fsm_user_info(self):
        return self._fsm_user_info

    @fsm_user_info.setter
    def fsm_user_info(self, fsm_user_info):
        self._fsm_user_info = fsm_user_info

    def send_action(self, action, fun, args, kwargs):
        return fun(*args, **kwargs)

    def change_state_to(self, state: State):
        state.fsm_user_info = self.fsm_user_info
        self.fsm_user_info.state = state


class StateEcho(State):

    def send_action(self, action: ActionForFSM, fun, args, kwargs):
        if isinstance(action, (ActionNotChangeState, ActionChangeStateToEcho)):
            return fun(*args, **kwargs)
        if isinstance(action, ActionChangeStateCommand):
            self.change_state_to(action.change_state_to())
            return fun(*args, **kwargs)


class StateConversation(State):
    sub_state_data_cash = {}

    def __init__(self):
        self.next_sub_state = self.sub_state_pass

    def send_action(self, action, fun, args, kwargs):
        self.change_state_to(action.change_state_to())
        return self.send_sub_state(fun, args, kwargs)

    def send_sub_state(self, fun, args, kwargs):
        return self.next_sub_state(fun, args, kwargs)

    # sub_state functions__________________________________________
    async def sub_state_pass(self, fun, args, kwargs):
        return fun(*args, **kwargs)


class ConcreteStateCreateUser(StateConversation):
    def __init__(self):
        self.next_sub_state = self._check_name

    def send_action(self, action, fun, args, kwargs):
        if isinstance(action, ActionMassage):
            return self.send_sub_state(fun, args, kwargs)
        if isinstance(action, ActionChangeStateCommand):
            self.change_state_to(action.change_state_to())
            return fun(*args, **kwargs)

    def send_sub_state(self, fun, args, kwargs):
        return self.next_sub_state(fun, args, kwargs)

    # sub_state functions__________________________________________
    async def _check_name(self, fun, args, kwargs):
        logging_user_name = args[0].text
        if check_user_logging_name(logging_user_name):
            self.sub_state_data_cash['logging_name'] = logging_user_name
            self.next_sub_state = self._enter_password
            return await args[0].reply('Enter your password:')
        else:
            self.next_sub_state = self._check_name
            return await args[0].reply('Logging name is already in use, try again. Enter new user logging name:')

    async def _enter_password(self, fun, args, kwargs):
        res = args[0].text
        hash_ = hashlib.sha256()
        salt = cfg.salt
        hash_.update((res + salt).encode('utf_8'))
        self.sub_state_data_cash['password'] = hash_.digest()
        self.next_sub_state = self._confirm_password
        return await args[0].reply('Confirm your password:')

    async def _confirm_password(self, fun, args, kwargs):
        res = args[0].text
        hash_confirm = hashlib.sha256()
        salt = cfg.salt
        hash_confirm.update((res + salt).encode('utf_8'))
        if hash_confirm.digest() == self.sub_state_data_cash['password']:
            new_user(self.sub_state_data_cash['logging_name'], hash_confirm.hexdigest(), args[0].sender_id)
            self.change_state_to(StateEcho())
            return await args[0].reply('User was created')
        else:
            self.next_sub_state = self._enter_password
            return await args[0].reply('Разные пароли. Try again. Enter your password:')


class ConcreteStateAddUser(StateConversation):
    pass


# ______________________________________________________________________________________________________________________
# Action classes for FSM

class ActionForFSM:
    pass


class ActionChangeStateCommand(ActionForFSM):
    def __init__(self, change_state_to):
        self.change_state_to = change_state_to


class ActionNotChangeState(ActionForFSM):
    pass


# ________________________________
# classes not change state:


class ActionMassage(ActionNotChangeState):
    pass


class ActionCommand(ActionNotChangeState):
    pass


# ________________________________
# classes change state:
class ActionChangeStateToConversation(ActionChangeStateCommand):
    pass


class ActionChangeStateToEcho(ActionChangeStateCommand):
    pass


# ______________________________________________________________________________________________________________________
# ParseBOT FSM
class UserInfo:
    def __init__(self, state: State, sender_id, data=None):
        self.state = state
        self.user_id = sender_id
        self.user_data = data


class ParseBotUsersStateFSM:
    users_info_for_parse_bot = {
    }

    def action_manager(self, action, fun, args, kwargs):
        sender_id = args[0].sender_id
        user_info = self.get_user_info(sender_id)
        return user_info.state.send_action(action, fun, args, kwargs)

    def get_user_info(self, sender_id):
        if self.users_info_for_parse_bot.get(sender_id, None) is None:
            new_user = UserInfo(StateEcho(), sender_id)
            self.users_info_for_parse_bot[sender_id] = new_user
            self.users_info_for_parse_bot[sender_id].state.fsm_user_info = new_user
        return self.users_info_for_parse_bot[sender_id]


# ______________________________________________________________________________________________________________________
# bot`s handlers


@telethon.events.register(telethon.events.NewMessage(pattern='/my_users'))
async def BOT_handler_my_users(event):
    users_list = get_all_users(event.sender_id)
    await event.reply(f'Your users: {users_list}')
    raise telethon.events.StopPropagation


@telethon.events.register(telethon.events.NewMessage(pattern='/set'))
async def BOT_handler_set_data(event):
    try:
        list_ = event.message.text.split(maxsplit=2)
        if len(list_) < 2:
            raise NotCorrectExc
        set__, data = list_[0:2]
        setlist_ = list_[0].split('_', maxsplit=2)
        if len(setlist_) < 3:
            raise NotCorrectExc
        _, user_logging, arg = setlist_

        set_data(event.sender_id, user_logging, arg, data)
        await event.reply(f"Данные сохранены: session '{user_logging}':{arg}: {data}")
    except NotCorrectExc as e:
        await event.reply('{}\n'
                          'Введена неправильная команда.\nExample: "/set_sessionname_*** value"\n*** - one of:\n{} for '
                          'start script;\n{} for other set'.format(e, arg_for_session, arg_other))
    except UserNotFoundExc as e:
        await event.reply(f'Пользователь не найден\n'
                          f'Чтобы создать ползователя используйте команду {command_dict["add_user"]}')
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
            raise NotCorrectExc
        _, user_logging, arg = getlist_

        value_arg = get_data(event.sender_id, user_logging, arg)
        await event.reply("session '{}':{}:: {}".format(user_logging, arg, value_arg))
    except NotCorrectExc as e:
        await event.reply('{}\nВведена неправильная команда.\n'
                          'Example: "/get_sessionname_***"\n*** - one of:\n {}'.format(e, command_get_list))

    except UserNotFoundExc as e:
        await event.reply(f'Пользователь не найден\n'
                          f'Чтобы создать ползователя используйте команду {command_dict["add_user"]}')

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
            raise NotCorrectExc
        add__, data = list_[0], list_[1:]
        addlist_ = add__.split('_', maxsplit=2)
        if len(addlist_) != 3:
            raise NotCorrectExc
        _, user_logging, arg = addlist_

        for i in data:
            set_data(event.sender_id, user_logging, arg, i)
        await event.reply(f"Данные сохранены: session '{user_logging}':{arg}: {data}")

    except NotCorrectExc as e:
        await event.reply('{}\nВведена неправильная команда.\n'
                          'Example: "/add_sessionname_*** value"\n*** - one of:\n{}'.format(e, arg_for_session,
                                                                                            arg_other))
    except DataDuplicateExc as e:
        await event.reply(f'{e}')

    except UserNotFoundExc as e:
        await event.reply(f'Пользователь не найден\n'
                          f'Чтобы создать ползователя используйте команду {command_dict["add_user"]}')

    except:
        await event.reply('Что-то пошло не так')
        raise
    finally:
        raise telethon.events.StopPropagation


@telethon.events.register(telethon.events.NewMessage(pattern='/start_script'))
async def BOT_handler_start_script(event):
    if all((cfg.api_hash, cfg.api_id, cfg.my_channel_id)):
        telegram_parse.add_client_to_loop(event.client, event.sender_id)
        await event.reply(f"Запущено!")
    raise telethon.events.StopPropagation


@telethon.events.register(telethon.events.NewMessage(pattern='/cancel|/start'))
@fsm_decor(ActionChangeStateToEcho(StateEcho))
async def BOT_handler_cancel(event):
    await event.client.send_message(event.sender_id, 'Echo mod active')
    raise telethon.events.StopPropagation


@telethon.events.register(telethon.events.NewMessage(pattern='/add_user'))
@fsm_decor(ActionChangeStateToConversation(ConcreteStateAddUser))
async def BOT_handler_add_user(event):
    pass


@telethon.events.register(telethon.events.NewMessage(pattern='/create_user'))
@fsm_decor(ActionChangeStateToConversation(ConcreteStateCreateUser))
async def BOT_handler_create_user(event):
    await event.reply('Enter new user logging name:')
    raise telethon.events.StopPropagation


@telethon.events.register(telethon.events.NewMessage)
@fsm_decor(ActionMassage())
async def BOT_handler_echo(event):
    await event.reply(event.text)
    raise telethon.events.StopPropagation


@telethon.events.register(telethon.events.NewMessage)
async def BOT_admin_handler_echo(event):
    await event.reply(event.text)
    raise telethon.events.StopPropagation


logger = my_logger.get_logger(__name__)

parse_bot_users_state_fsm = ParseBotUsersStateFSM()
