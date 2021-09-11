# -*- coding: utf-8 -*-
import BOT.test1.Bot_test4.data_value as data_value
import logging
import logging.config
import asyncio
import BOT.test1.Bot_test4.config_for_bot as cfg

# from BOT.test1.Bot_test4.Main_bot4_3 import bot_admin_sendms
__start = False


class AdminbotsendHandler(logging.Handler):
    def emit(self, record):
        if data_value.telegram_parse is None:
            return
        data_value.telegram_parse.send_bot_message_to(self.format(record))

    def __init__(self):
        logging.Handler.__init__(self)


def get_logger(name):
    logger = logging.getLogger(name)
    # mh = MyLogHandler()
    # mh.setLevel(level=logging.ERROR)
    # logger.addHandler(mh)
    return logger


if not __start:
    logging.config.fileConfig('logging.conf')
    logging.getLogger('urllib3').setLevel(logging.ERROR)
    logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.ERROR)
    # logging.getLogger('telethon.network.mtprotosender').setLevel(logging.ERROR)
    # logging.getLogger('telethon.extensions.messagepacker').setLevel(logging.ERROR)
    # logging.getLogger('asyncio').setLevel(logging.INFO)
    __start = True
