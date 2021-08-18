
# -*- coding: utf-8 -*-
from BOT.test1.Bot_test4 import handlers_USERBOT as h_ubot
from BOT.test1.Bot_test4 import handlers_BOT as h_bot


handlers_USERBOT_dict = {
    'event_handler_ms_from': h_ubot.event_handler_ms_from,
    'event_handler_spam_ms': h_ubot.event_handler_spam_ms
}

handlers_BOT_dict = {
    'BOT_handler_start_script': h_bot.BOT_handler_start_script,
    'BOT_handler_start': h_bot.BOT_handler_start,
    # 'BOT_handler_set_api_hash_and_id': h_bot.BOT_handler_set_api_hash_and_id,
    # 'BOT_handler_set_id_channel': h_bot.BOT_handler_set_id_channel,
    # 'BOT_handler_set_phone_number': h_bot.BOT_handler_set_phone_number,
    'BOT_handler_set_data': h_bot.BOT_handler_set_data,
    'BOT_handler_get_data': h_bot.BOT_handler_get_data,
    'BOT_handler_add_data': h_bot.BOT_handler_add_data,
    'BOT_handler_echo': h_bot.BOT_handler_echo
}

