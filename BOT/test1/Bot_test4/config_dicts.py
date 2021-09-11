
# -*- coding: utf-8 -*-
import BOT.test1.Bot_test4.handlers_BOT_user as h_ubot
import BOT.test1.Bot_test4.handlers_BOTS as h_bot


handlers_USERBOT_dict = {
    'event_handler_ms_from': h_ubot.event_handler_ms_from,
    'event_handler_spam_ms': h_ubot.event_handler_spam_ms,
}

handlers_BOT_parse_dict = {
    'BOT_handler_start_script': h_bot.BOT_handler_start_script,
    # 'BOT_handler_start': h_bot.BOT_handler_start,
    'BOT_handler_create_user': h_bot.BOT_handler_create_user,
    'BOT_handler_add_user': h_bot.BOT_handler_add_user,
    'BOT_handler_cancel': h_bot.BOT_handler_cancel,
    'BOT_handler_my_users': h_bot.BOT_handler_my_users,
    # 'BOT_handler_set_api_hash_and_id': h_bot.BOT_handler_set_api_hash_and_id,
    # 'BOT_handler_set_id_channel': h_bot.BOT_handler_set_id_channel,
    # 'BOT_handler_set_phone_number': h_bot.BOT_handler_set_phone_number,
    'BOT_handler_set_data': h_bot.BOT_handler_set_data,
    'BOT_handler_get_data': h_bot.BOT_handler_get_data,
    'BOT_handler_add_data': h_bot.BOT_handler_add_data,
    'BOT_handler_echo': h_bot.BOT_handler_echo,
}

handlers_BOT_admin_dict = {
    'BOT_handler_echo': h_bot.BOT_admin_handler_echo,
}

handlers_BOT_dict = {
    'bot_admin': handlers_BOT_admin_dict,
    'bot_parse': handlers_BOT_parse_dict,
    'bot_user': handlers_USERBOT_dict,
}