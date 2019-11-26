from telegram import InlineKeyboardButton
from json import dumps


class InlineHandler:
    def __init__(self, mark, handle):
        self.mark = mark
        self.handle = handle

    def generate_btn(self, value, text):
        return InlineKeyboardButton(text=text, callback_data=dumps({'mk': self.mark, 'v': value}))
