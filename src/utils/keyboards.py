import emoji
from telebot import types


def create_keyboard(*keys, row_width=2, resize_keyboard=True):
    """ Create keyboard with buttons """
    
    markup = types.ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=resize_keyboard)
    
    keys = map(emoji.emojize, keys)
    buttons = map(types.KeyboardButton, keys)
    markup.add(*buttons)
    return markup
    