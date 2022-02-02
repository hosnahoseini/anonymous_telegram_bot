import os

import telebot
from emoji import emojize
from loguru import logger

from src.bot import bot
from src.constants import keyboards
from src.data import DATA_DIR
from src.filters import IsAdmin
from src.utils.io import write_json


class Bot:
    """
    Template for telegram bot
    """
    def __init__(self, telebot):
        self.bot = telebot

        # register filter
        bot.add_custom_filter(IsAdmin())

        # add handlers
        self.handlers()

        # start bot
        logger.info('Bot is running')
        self.bot.infinity_polling()
    
    def handlers(self):

        @bot.message_handler(is_admin=True)
        def admin_of_group(message):
            self.send_message(message.chat.id, 'You are admin of this group!')

        @self.bot.message_handler(func=lambda message: True)
        def echo_all(message):
            self.send_message(
                message.chat.id,
                f'<strong>your message is:</strong> {message.text}',
                reply_markup=keyboards.main
            )


    def send_message(self, chat_id, text, reply_markup=None, emoji=True):
        if emoji:
            text = emojize(text, use_aliases=True)
        
        self.bot.send_message(chat_id, text, reply_markup=reply_markup)

if __name__ == '__main__':
    logger.info('Bot started')
    bot = Bot(telebot=bot)
    logger.info('Bot stopped')

