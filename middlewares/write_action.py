from telegram import ChatAction
from utils.properties_telegram import get_chat_id


def write_action(f):
    def wrapped(*args, **kwargs):
        [self, bot, update] = args
        bot.send_chat_action(chat_id=get_chat_id(update), action=ChatAction.TYPING)
        f(*args, **kwargs)

    return wrapped
