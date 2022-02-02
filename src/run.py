import os

import telebot
from emoji import emojize
from loguru import logger

from src.bot import bot
from src.constants import keyboards, keys, states
from src.db import db
from src.filters import IsAdmin


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

        @bot.message_handler(commands=['start'])
        def start(message):
            """ Start"""
            self.send_message(
                message.chat.id,
                f"Hey {message.chat.first_name}",
            )

            db.users.update_one(
                {'chat.id': message.chat.id},
                {'$set': message.json},
                upsert=True
                )
            self.update_state(message.chat.id, states.main)
                 
        @bot.message_handler(regexp=emojize(keys.random_connect))
        def random_connect(message):
            """ Random Connect"""

            self.send_message(
                message.chat.id,
                 ':bust_in_silhouette: Random connect you to other user ...',
                 reply_markup=keyboards.exit)  
            self.update_state(message.chat.id, states.random_connect)
            other_user = db.users.find_one({
                'state': states.random_connect,
                'chat.id': {'$ne': message.chat.id}
                })

            if not other_user:
                return

            self.update_state(other_user['chat']['id'], states.connected)
            self.send_message(other_user['chat']['id'], f'{message.chat.id} connected you')
            
            self.update_state(message.chat.id, states.connected)
            self.send_message(message.chat.id, f"{other_user['chat']['id']} connected you")

            db.users.update_one(
                {'chat.id': message.chat.id},
                {'$set': {'connected_to': other_user['chat']['id']}}  
            )

            db.users.update_one(
                {'chat.id': other_user['chat']['id']},
                {'$set': {'connected_to': message.chat.id}}
            )


        @bot.message_handler(regexp=emojize(keys.exit))
        def exit(message):
            """ Exit from connection"""

            # update state and send message to my user
            self.send_message(
                message.chat.id,
                 keys.exit,
                 reply_markup=keyboards.main)
            self.update_state(message.chat.id, states.main)

            # update state and send message to other user
            try:
                connected_to = db.users.find_one({'chat.id': message.chat.id})['connected_to']
            except KeyError:
                return
            
            if not connected_to:
                return

            self.send_message(
            connected_to,
            keys.exit,
            reply_markup=keyboards.main)
            self.update_state(connected_to, states.main) 
        
            # remove connected_to
            db.users.update_one(
                {'chat.id': message.chat.id},
                {'$set': {'connected_to': None}}
            )
            db.users.update_one(
                {'chat.id': connected_to},
                {'$set': {'connected_to': None}}
            )

        @self.bot.message_handler(func=lambda message: True)
        def echo(message):
            """
            Echo message to other user
            """
            user = db.users.find_one({'chat.id': message.chat.id})

            if not user or user['state'] != states.connected or not user['connected_to']:
                return

            self.send_message(
                user['connected_to'],
                message.text,
                reply_markup=keyboards.exit
            )
            


    def send_message(self, chat_id, text, reply_markup=None, emoji=True):
        if emoji:
            text = emojize(text, use_aliases=True)
    
        self.bot.send_message(chat_id, text, reply_markup=reply_markup)
    
    def update_state(self, chat_id, state):
        db.users.update_one(
            {'chat.id': chat_id},
            {'$set': {'state': state}},
            upsert=True
        )

if __name__ == '__main__':
    logger.info('Bot started')
    bot = Bot(telebot=bot)
    logger.info('Bot stopped')
